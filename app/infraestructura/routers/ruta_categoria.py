from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Annotated, List

from app.core.security import validarRolAdmin
from app.dominio.modelos.categoria import Categoria
from app.infraestructura.basedatos.db import get_db
from app.infraestructura.repositorios.categoria_repositorio import CategoriaRepositorio


routerCategorias = APIRouter()

@routerCategorias.get('/',
    response_model=List[Categoria],
    summary="Obtener listado de categorías",
    description="Lista las categorías registradas en el sistema",
    response_description="Obtiene lista de categorías"
)
def obtener_categorias(db: Session = Depends(get_db)):
    categorias_db = CategoriaRepositorio(db=db).obtener_categorias()
    categorias = [Categoria.model_validate(cliente) for cliente in categorias_db]
    return JSONResponse(content=jsonable_encoder(categorias))


@routerCategorias.post('/',
    response_model=Categoria,
    summary="Crear categoría",
    description="Crea una categoría en el sistema si el usuario autenticado tiene permisos de administrador",
    response_description="Obtiene la categoría creada"
)
def crear_categoria(categoria_creacion: Categoria, permiso: Annotated[bool, Depends(validarRolAdmin)], db: Session = Depends(get_db)):
    if permiso:
        try:
            categoria_nueva = CategoriaRepositorio(db=db).crear_categoria(categoria_creacion)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(Categoria.model_validate(categoria_nueva)))
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La categoria ya existe') from e
