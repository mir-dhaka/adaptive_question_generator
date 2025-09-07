import logging
from logging import Logger
from sqlalchemy.orm import Session
from app.models.dag_models import DAG, DAGEdge, KC, KCTopic
from app.schemas.dag_schemas import DAGBase, DAGOut, DAGEdgeBase, DAGEdgeOut
from app.infra.response_handlers import OkResponse, BadRequestException, ResourceNotFoundException


class DAGService:
    @staticmethod
    def create_dag(dag_data: DAGBase, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Creating DAG: title={dag_data.title}")

        existing = db.query(DAG).filter(DAG.title == dag_data.title).first()
        if existing:
            logger.warning("DAG with this title already exists")
            raise BadRequestException("DAG with this title already exists.")

        new_dag = DAG(
            title=dag_data.title,
            summary=dag_data.summary
        )
        db.add(new_dag)
        db.commit()
        db.refresh(new_dag)

        logger.info(f"Created DAG with ID {new_dag.id}")
        return OkResponse(DAGOut.from_orm(new_dag))

    @staticmethod
    def get_dag(dag_id: int, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Fetching DAG ID {dag_id}")

        dag = db.query(DAG).get(dag_id)
        if not dag:
            logger.warning(f"DAG ID {dag_id} not found")
            raise ResourceNotFoundException("DAG not found.")

        return OkResponse(DAGOut.from_orm(dag))

    @staticmethod
    def update_dag(dag_id: int, dag_data: DAGBase, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Updating DAG ID {dag_id}")

        dag = db.query(DAG).get(dag_id)
        if not dag:
            logger.warning(f"DAG ID {dag_id} not found")
            raise ResourceNotFoundException("DAG not found.")

        for field, value in dag_data.dict(exclude_unset=True).items():
            setattr(dag, field, value)

        db.commit()
        db.refresh(dag)

        logger.info(f"Updated DAG ID {dag_id}")
        return OkResponse(DAGOut.from_orm(dag))

    @staticmethod
    def delete_dag(dag_id: int, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Deleting DAG ID {dag_id}")

        dag = db.query(DAG).get(dag_id)
        if not dag:
            logger.warning(f"DAG ID {dag_id} not found")
            raise ResourceNotFoundException("DAG not found.")

        db.delete(dag)
        db.commit()

        logger.info(f"Deleted DAG ID {dag_id}")
        return OkResponse(message=f"DAG ID {dag_id} deleted successfully.")

    @staticmethod
    def list_dags(db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info("Listing all DAGs")

        dags = db.query(DAG).all()
        dags_out = [DAGOut.from_orm(d) for d in dags]

        return OkResponse({"dags": dags_out})

    # ----------------------------
    # DAG Edge CRUD
    # ----------------------------

    @staticmethod
    def add_edge(edge_data: DAGEdgeBase, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Adding edge: DAG={edge_data.dag_id}, from={edge_data.from_kc_id}, to={edge_data.to_kc_id}")

        dag = db.query(DAG).get(edge_data.dag_id)
        if not dag:
            raise ResourceNotFoundException("DAG not found.")

        from_kc = db.query(KC).get(edge_data.from_kc_id)
        to_kc = db.query(KC).get(edge_data.to_kc_id)
        if not from_kc or not to_kc:
            raise BadRequestException("Both from_kc_id and to_kc_id must reference valid KCs.")

        new_edge = DAGEdge(
            dag_id=edge_data.dag_id,
            from_kc_id=edge_data.from_kc_id,
            to_kc_id=edge_data.to_kc_id
        )
        db.add(new_edge)
        db.commit()
        db.refresh(new_edge)

        logger.info(f"Added edge ID {new_edge.id}")
        return OkResponse(DAGEdgeOut.from_orm(new_edge))

    @staticmethod
    def remove_edge(edge_id: int, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Removing edge ID {edge_id}")

        edge = db.query(DAGEdge).get(edge_id)
        if not edge:
            raise ResourceNotFoundException("Edge not found.")

        db.delete(edge)
        db.commit()

        logger.info(f"Removed edge ID {edge_id}")
        return OkResponse(message=f"Edge ID {edge_id} deleted successfully.")
