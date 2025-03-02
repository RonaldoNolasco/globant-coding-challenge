import pandas as pd
import io
from fastapi import HTTPException
from sqlmodel import select
from app.models import Department, Job, Employee

def process_data(session, model, df, *columns):
    existing_records = {record.id: record for record in session.exec(select(model)).all()}
    incoming_ids = set(df["id"].astype(int))
    existing_ids = set(existing_records.keys())
    
    inserted = 0
    updated = 0
    deleted = 0
    
    for _, row in df.iterrows():
        record_id = int(row["id"])
        if record_id in existing_records:
            record = existing_records[record_id]
            for col in columns[1:]:
                setattr(record, col, row[col])
            updated += 1
        else:
            session.add(model(**{col: row[col] for col in columns}))
            inserted += 1
    
    for record_id in existing_ids - incoming_ids:
        session.delete(existing_records[record_id])
        deleted += 1
    
    session.commit()
    return {"message": "Data processed successfully", "inserted": inserted, "updated": updated, "deleted": deleted}
