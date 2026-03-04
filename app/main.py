from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
import uuid

app = FastAPI(title="Inventario API", version="1.0.0")

# ──────────────────────────────────────────────
# Modelo de datos
# ──────────────────────────────────────────────
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(ge=0)
    quantity: int = Field(ge=0, default=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, ge=0)

class Product(ProductBase):
    id: str

# ──────────────────────────────────────────────
# Almacén en memoria (diccionario)
# ──────────────────────────────────────────────
products_db: dict[str, Product] = {}

# Datos de ejemplo para que la primera consulta no esté vacía
_sample_products = [
    {"name": "Laptop", "description": "Laptop 15 pulgadas", "price": 15999.99, "quantity": 10},
    {"name": "Mouse", "description": "Mouse inalámbrico", "price": 299.50, "quantity": 50},
    {"name": "Teclado", "description": "Teclado mecánico RGB", "price": 1200.00, "quantity": 30},
]

for p in _sample_products:
    _id = str(uuid.uuid4())
    products_db[_id] = Product(id=_id, **p)

# ──────────────────────────────────────────────
# Endpoints CRUD
# ──────────────────────────────────────────────

@app.get("/products/", response_model=list[Product])
def list_products(limit: int = Query(20, ge=1), offset: int = Query(0, ge=0)):
    """Devuelve la lista de productos con paginación."""
    all_products = list(products_db.values())
    return all_products[offset : offset + limit]


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    """Obtiene un producto por su ID."""
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@app.post("/products/", response_model=Product, status_code=201)
def create_product(data: ProductCreate):
    """Crea un nuevo producto."""
    product_id = str(uuid.uuid4())
    product = Product(id=product_id, **data.model_dump())
    products_db[product_id] = product
    return product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: str, data: ProductUpdate):
    """Actualiza un producto existente."""
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    update_data = data.model_dump(exclude_unset=True)
    updated = product.model_copy(update=update_data)
    products_db[product_id] = updated
    return updated


@app.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: str):
    """Elimina un producto por su ID."""
    product = products_db.pop(product_id, None)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"detail": "Producto eliminado", "id": product_id}
