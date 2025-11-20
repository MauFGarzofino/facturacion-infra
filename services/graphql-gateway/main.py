import strawberry
from typing import List, Optional
import httpx
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# --- 1. DEFINICIÓN DE TIPOS ---

@strawberry.type
class User:
    id: str
    username: str
    email: str

@strawberry.type
class Empresa:
    id: str
    razon_social: str
    nit: str
    cufd_vigente: Optional[str] = None

@strawberry.type
class Factura:
    cuf: str
    fecha_emision: str
    monto_total: float
    estado: str
    empresa_id: str 
    usuario_id: str

@strawberry.type
class Notificacion:
    id: int
    mensaje: str
    leida: bool

# --- 2. RESOLVERS (CONECTADOS A TUS MICROSERVICIOS REALES) ---

async def get_users_from_auth() -> List[User]:
    # Contenedor: auth-service | Puerto: 8000
    url = "http://auth-service:8000/users" 
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url)
            if res.status_code == 200:
                # Nota: Tu Auth Service devuelve "_id", aquí lo mapeamos a "id"
                return [User(id=str(u["_id"]), username=u["username"], email=u["email"]) for u in res.json()]
        except Exception as e:
            print(f"⚠️ Error Auth Service: {e}")
        return []

async def get_empresas_from_nest() -> List[Empresa]:
    # Contenedor: servicio-empresas-cufd | Puerto: 3000 (Estándar NestJS)
    # RUTA PENDIENTE: Verifica si es /empresas o /api/empresas
    url = "http://servicio-empresas-cufd:3000/empresas"
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url)
            if res.status_code == 200:
                data = res.json()
                return [
                    Empresa(
                        id=str(e.get("id", "")), 
                        razon_social=e.get("razon_social", "Sin Nombre"), 
                        nit=e.get("nit", "0"),
                        cufd_vigente=e.get("cufd")
                    ) for e in data
                ]
        except Exception as e:
            print(f"⚠️ Error Empresas (NestJS): {e}")
        return []

async def get_facturas_from_go() -> List[Factura]:
    # Contenedor: recepcion_facturacion | Puerto: 8080 (Estándar Go)
    url = "http://recepcion_facturacion:8080/facturas"
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url)
            if res.status_code == 200:
                data = res.json()
                return [
                    Factura(
                        cuf=f.get("cuf", ""),
                        fecha_emision=f.get("fecha", ""),
                        monto_total=float(f.get("monto", 0)),
                        estado=f.get("estado", "Desconocido"),
                        empresa_id=str(f.get("empresa_id", "")),
                        usuario_id=str(f.get("usuario_id", ""))
                    ) for f in data
                ]
        except Exception as e:
            print(f"⚠️ Error Facturación (Go): {e}")
        return []

async def get_notificaciones_from_laravel() -> List[Notificacion]:
    # Contenedor: notifications | Puerto: 8000 (Visto en tu docker-compose)
    url = "http://notifications:8000/api/notificaciones" # Laravel suele usar prefijo /api
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url)
            if res.status_code == 200:
                data = res.json()
                return [
                    Notificacion(
                        id=int(n.get("id", 0)),
                        mensaje=n.get("mensaje", ""),
                        leida=bool(n.get("leida", False))
                    ) for n in data
                ]
        except Exception as e:
            print(f"⚠️ Error Notificaciones (Laravel): {e}")
        return []

# --- 3. QUERY PRINCIPAL ---

@strawberry.type
class Query:

    # Proxies directos
    @strawberry.field
    async def users(self) -> List[User]:
        return await get_users_from_auth()

    @strawberry.field
    async def empresas(self) -> List[Empresa]:
        return await get_empresas_from_nest()

    @strawberry.field
    async def facturas(self) -> List[Factura]:
        return await get_facturas_from_go()
        
    @strawberry.field
    async def notificaciones(self) -> List[Notificacion]:
        return await get_notificaciones_from_laravel()

    # Consulta Combinada (Ejemplo de integración)
    @strawberry.field
    async def reporte_completo(self) -> List[str]:
        facturas = await get_facturas_from_go()
        empresas = await get_empresas_from_nest()
        
        # Mapa para buscar rápido el nombre de la empresa
        mapa_empresas = {str(e.id): e.razon_social for e in empresas}
        
        reporte = []
        for f in facturas:
            empresa = mapa_empresas.get(f.empresa_id, "Empresa Desconocida")
            reporte.append(f"Factura {f.cuf} ({f.monto_total} Bs) - Emitida por: {empresa}")
        return reporte

# --- 4. CONFIGURACIÓN APP ---

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI(title="SIAT Gateway GraphQL")
app.include_router(graphql_app, prefix="/graphql")

@app.get("/health")
async def health_check():
    return {"status": "ok"}