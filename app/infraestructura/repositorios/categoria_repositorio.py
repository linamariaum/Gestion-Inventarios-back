from sqlalchemy.orm import Session

from app.dominio.modelos.categoria import Categoria
from app.infraestructura.basedatos.entidades.categoria_entidad import Categoria as CategoriaEntidad


class CategoriaRepositorio:
    def __init__(self, db: Session):
        self.db = db


    def crear_categoria(self, categoria: Categoria) -> CategoriaEntidad:
        categoria_creacion = CategoriaEntidad(**categoria.model_dump())
        self.db.add(categoria_creacion)
        self.db.commit()
        self.db.refresh(categoria_creacion)
        return categoria_creacion


    def obtener_categorias(self)-> CategoriaEntidad:
        return self.db.query(CategoriaEntidad).all()
    

    def obtener_categoria(self, categoria_id: int)-> CategoriaEntidad:
        return self.db.query(CategoriaEntidad).filter(CategoriaEntidad.id == categoria_id).first()


    def existe_categoria(self, categoria_id: int) -> bool:
        return self.db.query(CategoriaEntidad).filter(CategoriaEntidad.id == categoria_id).first() is not None
