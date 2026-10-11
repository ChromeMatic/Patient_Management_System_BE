from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from database_config.db_config import get_db
from user_authenication.auth_service import verify_jwt_access_token
from sys_reports.report_services import grenerate_basic_pdf_report


report_endpoint = APIRouter( prefix="/Report",tags=["Report Endpoints"])
db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bear = OAuth2PasswordBearer(tokenUrl='auth/token')


@report_endpoint.get("/Reports",status_code=status.HTTP_200_OK)
def Fetch_pdf_report(db:db_dependency,token:Annotated[str,Depends(oauth2_bear)]):
    user_info = verify_jwt_access_token(jwt_token=token,db=db)

    if user_info not in ['supervisor','admin','doctor','nurse']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized to view data"
        )
    else:
        result = grenerate_basic_pdf_report(db=db)
        return StreamingResponse(
                    result,
                    media_type="application/pdf",
                    headers={
                        "Content-Disposition": f"attachment; filename=Report.pdf"
                    }
        )