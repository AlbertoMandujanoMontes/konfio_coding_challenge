"""Clean XCom data after dag execution."""
import logging
from airflow.utils.db import provide_session
from airflow.models import XCom
import pendulum


# Cleaning all saved data at metadata db after this execution
@provide_session
def cleanup(context, session=None):
    """
    Clean the XCOM data stored during the dag execution.

    :param context: Dag execution context
    :param session: Airflow session
    :return: None
    """
    logging.info("Cleaning session xcom data for dag {} on {}".format(
        context['dag'].dag_id,
        pendulum.parse(context["ts"])
    ))
    session.query(XCom).filter(
        XCom.dag_id == context['dag'].dag_id,
        XCom.execution_date == pendulum.parse(context["ts"])
    ).delete()
    session.commit()
