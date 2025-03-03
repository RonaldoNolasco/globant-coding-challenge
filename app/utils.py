import pandas as pd
import io
from fastapi import HTTPException
from sqlmodel import select, SQLModel
from app.models import Department, Job, Employee
from typing import Type

# Funcion para obtener una clase, segun el tipo de modelo enviado
def get_model_metadata(model: Type[SQLModel]):
    """ Devuelve los nombres de los atributos del modelo y sus tipos de datos. """
    return {field_name: field_info.annotation for field_name, field_info in model.model_fields.items()}

# Funcion para procesar los datos del csv cargado
def process_data(session, model, df, *columns):
    # Se obtienen aquellos id existentes en la tabla
    existing_records = {record.id: record for record in session.exec(select(model)).all()}

    # Se obtienen los id que llegan en el archivo
    incoming_ids = set(df["id"].astype(int))

    # Se obtienen los id que existen en la tabla
    existing_ids = set(existing_records.keys())
    
    # Se definen contadores para registros insertados, actualizados o eliminados
    inserted = 0
    updated = 0
    deleted = 0
    
    # Se iteran por todas las filas del archivo
    for _, row in df.iterrows():
        # Se obtiene el id de la fila
        record_id = int(row["id"])

        # Si el id ya ha sido insertado, es manejado como actualizacion
        if record_id in existing_records: 

            # Se ubica el registro ya insertado
            record = existing_records[record_id]

            # Se iteran por todos los campos del registro
            for col in columns[1:]:
                # Se actualizan los valores de todos los campos
                setattr(record, col, row[col])
            # Incrementa la cantidad de registros actualizados
            updated += 1
        
         # Caso contrario, es manejado como una insercion
        else:
            # El objeto es agregado a la tabla
            session.add(model(**{col: row[col] for col in columns}))
            # Se incrementa la cantidad de registros insertados
            inserted += 1
    
    # Se iteran sobre aquellos id que existen en la tabla pero no en el archivo
    for record_id in existing_ids - incoming_ids:
        # Son eliminados esos registros
        session.delete(existing_records[record_id])
        # Se incrementa la cantidad de registros eliminados
        deleted += 1
    
    # Se commitea en la base de datos
    session.commit()
    return {"message": "Data processed successfully", "inserted": inserted, "updated": updated, "deleted": deleted}
