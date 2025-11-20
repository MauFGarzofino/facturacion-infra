import strawberry
from typing import List, Optional
import httpx
from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter

# ============================================================
# 1. DEFINICIÓN DE TIPOS GRAPHQL
# ============================================================

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


# ============================================================
# 2. RESOLVERS QUE CONSUMEN TUS MICROSERVICIOS
# ============================================================

# --- Auth Service (no requiere token) ---
async def get_users_from_auth() -> List[User]:
    url = "http://auth-service:8000/users"
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url)
            if res.status_code == 200:
                return [
                    User(
                        id=str(u["_id"]),
                        username=u["username"],
                        email=u["email"],
                    )
                    for u in res.json()
                ]
        except Exception as e:
            print(f"⚠️ Error Auth Service: {e}")

    return []


# --- Empresas (NestJS) *PROTEGIDO* ---
async def get_empresas_from_nest(info) -> List[Empresa]:
    token = info.context["request"].headers.get("authorization")

    url = "http://servicio-empresas-cufd:3000/empresas"
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, headers={"Authorization": token})
            if res.status_code == 200:
                return [
                    Empresa(
                        id=str(e.get("_id", "")),
                        razon_social=e.get("razonSocial", "Sin Nombre"),
                        nit=e.get("nit", "0"),
                        cufd_vigente=e.get("cufd"),
                    )
                    for e in res.json()
                ]
        except Exception as e:
            print(f"⚠️ Error Empresas (NestJS): {e}")

    return []

# --- Facturación GO *PROTEGIDO* ---
async def get_facturas_from_go(info) -> List[Factura]:
    token = info.context["request"].headers.get("authorization")

    url = "http://recepcion_facturacion:3002/api/v1/facturacion/facturas"
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, headers={"Authorization": token})
            if res.status_code == 200:
                return [
                    Factura(
                        cuf=f.get("cuf", ""),
                        fecha_emision=f.get("fecha", ""),
                        monto_total=float(f.get("monto", 0)),
                        estado=f.get("estado", "Desconocido"),
                        empresa_id=str(f.get("empresa_id", "")),
                        usuario_id=str(f.get("usuario_id", "")),
                    )
                    for f in res.json()
                ]
        except Exception as e:
            print(f"⚠️ Error Facturación (Go): {e}")

    return []


# --- Notificaciones Laravel (no requiere token) ---
async def get_notificaciones_from_laravel() -> List[Notificacion]:
    url = "http://notifications:8000/api/notificaciones"
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url)
            if res.status_code == 200:
                return [
                    Notificacion(
                        id=int(n.get("id", 0)),
                        mensaje=n.get("mensaje", ""),
                        leida=bool(n.get("leida", False)),
                    )
                    for n in res.json()
                ]
        except Exception as e:
            print(f"⚠️ Error Notificaciones (Laravel): {e}")

    return []


# ============================================================
# 3. SCHEMA DE QUERIES
# ============================================================

@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> List[User]:
        return await get_users_from_auth()

    @strawberry.field
    async def empresas(self, info) -> List[Empresa]:
        return await get_empresas_from_nest(info)

    @strawberry.field
    async def facturas(self, info) -> List[Factura]:
        return await get_facturas_from_go(info)

    @strawberry.field
    async def notificaciones(self) -> List[Notificacion]:
        return await get_notificaciones_from_laravel()

    @strawberry.field
    async def reporte_completo(self, info) -> List[str]:
        facturas = await get_facturas_from_go(info)
        empresas = await get_empresas_from_nest(info)

        mapa_empresas = {e.id: e.razon_social for e in empresas}

        return [
            f"Factura {f.cuf} ({f.monto_total} Bs) - Emitida por: {mapa_empresas.get(f.empresa_id, 'Empresa Desconocida')}"
            for f in facturas
        ]


# ============================================================
# 4. CONFIGURACIÓN APIS Y CONTEXTOS
# ============================================================

schema = strawberry.Schema(query=Query)

async def get_context(request: Request):
    return {"request": request}

graphql_app = GraphQLRouter(
    schema=schema,
    context_getter=get_context,
)

app = FastAPI(title="SIAT Gateway GraphQL")
app.include_router(graphql_app, prefix="/graphql")


@app.get("/health")
async def health_check():
    return {"status": "ok"}