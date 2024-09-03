from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Archivo(db.Model):
    __tablename__ = 'archivos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_publicacion = db.Column(db.DateTime(6), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    nombre_periodico = db.Column(db.String(255), nullable=False)
    ruta = db.Column(db.String(255), nullable=False)
    tiempo_procesamiento_ia = db.Column(db.Float)
    fecha_procesamiento_ia = db.Column(db.DateTime)
    tiempo_procesamiento_ocr = db.Column(db.Float)
    fecha_procesamiento_ocr = db.Column(db.DateTime)
    divisiones_politicas = db.relationship('DivisionPolitica', backref='archivo', lazy=True)
    unidades_militares = db.relationship('UnidadMilitar', backref='archivo', lazy=True)



class DivisionPolitica(db.Model):
    __tablename__ = 'divisiones_politicas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    archivo_id = db.Column(db.Integer, db.ForeignKey('archivos.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)



class UnidadMilitar(db.Model):
    __tablename__ = 'unidades_militares'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    archivo_id = db.Column(db.Integer, db.ForeignKey('archivos.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
