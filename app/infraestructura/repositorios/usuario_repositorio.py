from app.dominio.entidades.usuario_entidad import UsuarioEntidad

class UsuarioRepositorio:
    # def __init__(self, db: Session):
    #     self.db = db

    def obtener_usuario(self, username: str): #-> UsuarioEntidad:
        return username
        #return self.db.query(UsuarioEntidad).filter(UsuarioEntidad.id == username).first()

    fake_users_db = {
        "johndoe": {
            "username": "exito",
            "rol": "cliente",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW" # clave: secret
        },
        "alice": {
            "username": "jumbo",
            "rol": "cliente",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW" # clave: secret
        },
        "admin": {
            "username": "admin",
            "rol": "admin",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW" # clave: secret
        } 
    }
    @classmethod
    def fake_obtener_usuario(cls, username: str): # TODO borrar
        if username in cls.fake_users_db: # Si el usuario existe en db
            user_dict = cls.fake_users_db[username]
            return user_dict

#     def create_user(self, user: UserCreate) -> User:
#         db_user = User(**user.dict())
#         self.db.add(db_user)
#         self.db.commit()
#         self.db.refresh(db_user)
#         return db_user

#     def update_user(self, user_id: int, user: UserUpdate) -> User:
#         db_user = self.get_user(user_id)
#         if db_user:
#             for key, value in user.dict(exclude_unset=True).items():
#                 setattr(db_user, key, value)
#             self.db.commit()
#             self.db.refresh(db_user)
#         return db_user

#     def delete_user(self, user_id: int) -> User:
#         db_user = self.get_user(user_id)
#         if db_user:
#             self.db.delete(db_user)
#             self.db.commit()
#         return db_user