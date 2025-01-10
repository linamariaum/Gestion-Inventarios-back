
# class ClienteRepositorio:
#     def __init__(self, db: Session):
#         self.db = db

#     def obtener_cliente(self, user_id: int) -> Cliente:
#         return self.db.query(Cliente).filter(User.id == user_id).first()

#     def obtener_clientes(self, skip: int = 0, limit: int = 10) -> list[Cliente]:
#         return self.db.query(Cliente).offset(skip).limit(limit).all()

#     def crear_cliente(self, user: UserCreate) -> Cliente:
#         db_user = User(**user.dict())
#         self.db.add(db_user)
#         self.db.commit()
#         self.db.refresh(db_user)
#         return db_user

#     def actualizar_cliente(self, user_id: int, user: UserUpdate) -> Cliente:
#         db_user = self.obtener_cliente(user_id)
#         if db_user:
#             for key, value in user.dict(exclude_unset=True).items():
#                 setattr(db_user, key, value)
#             self.db.commit()
#             self.db.refresh(db_user)
#         return db_user

#     def eliminar_cliente(self, user_id: int) -> Cliente:
#         db_user = self.obtener_cliente(user_id)
#         if db_user:
#             self.db.delete(db_user)
#             self.db.commit()
#         return db_user
