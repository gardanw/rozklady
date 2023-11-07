from datetime import time

from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

import app.schemas
from app.models import RunStop, Busline, Run


def find_way(
    db: Session,
    dep_stop: app.schemas.StopInDB,
    arr_stop: app.schemas.StopInDB,
    dep_time: time,
):
    rs_dep = aliased(RunStop)
    rs_arr = aliased(RunStop)
    result = (
        (
            db.query(
                func.to_char(rs_dep.depart_time, "HH24:MI").label("rs_t_dep"),
                func.to_char(rs_arr.arrival_time, "HH24:MI").label("rs_t_arr"),
                Busline.busline_name,
                Run.descript,
            )
            .filter(
                rs_dep.stop_id == dep_stop.id,
                rs_arr.stop_id == arr_stop.id,
                rs_dep.depart_time < rs_arr.arrival_time,
                rs_dep.depart_time >= dep_time,
            )
            .join(rs_arr, rs_arr.run_id == rs_dep.run_id)
            .join(Run, Run.id == rs_dep.run_id)
            .join(Busline, Busline.id == Run.busline_id)
        )
        .order_by("rs_t_dep")
        .all()
    )
    return result
