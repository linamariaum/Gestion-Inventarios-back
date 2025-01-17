from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Annotated, List
import csv
from io import StringIO

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


@routerCategorias.post('/carga-masiva',
    summary="Carga masiva de categorías",
    description="Carga masiva de categorías desde un archivo CSV",
    response_description="Carga masiva de categorías",
    status_code=status.HTTP_201_CREATED
)
def crear_categorias_carga_masiva(permiso: Annotated[bool, Depends(validarRolAdmin)], file: UploadFile = File(...), db: Session = Depends(get_db)):
    if permiso:
        try:
            categorias = []
            content = StringIO(file.file.read().decode('utf-8'))
            reader = csv.DictReader(content)
            for row in reader:
                if 'nombre' not in row:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo CSV no contiene la columna 'nombre'")
                categoria = Categoria(nombre=row['nombre'].upper())
                if not CategoriaRepositorio(db=db).existe_categoria_por_nombre(categoria.nombre):
                    categorias.append(categoria)
            if categorias:
                CategoriaRepositorio(db=db).crear_categorias(categorias)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={'detail': 'Categorías cargadas exitosamente'})
        except IntegrityError as e:
            if "UNIQUE constraint" in str(e.orig):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Una o más categorías ya existen') from e
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error en la carga masiva de categorías') from e
        except KeyError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Error en el archivo CSV: columna {str(e)} no encontrada') from e
