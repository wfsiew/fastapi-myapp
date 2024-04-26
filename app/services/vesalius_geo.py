from zeep import AsyncClient, Settings
from fastapi import HTTPException
import xmltodict

from app.models import Patient, VesaliusWSException
from app.config import settings
from app import utils

logger = utils.getLogger('vesalius_geo')

class VesaliusGeoService:
    
    async def login(self) -> str:
        try:
            raise Exception('wrong')
        
        except Exception as e:
            logger.error(msg=str(e))
            
        cli = self.__getClient('AUTHENTICATION/Login.cfc')
        prm = {
            'company_code': settings.vesaliusServerCompanyCode,
            'system_code': settings.vesaliusServerSystemCode,
            'password': settings.vesaliusServerPassword
        }
        result = await cli.service.login(**prm)
        if result is None:
            raise HTTPException(status_code=204, detail='')
        
        res = self.__parseXML(result)
        data_dict = xmltodict.parse(res)
        if data_dict.get('Result') is not None and data_dict.get('Result').get('Error') is not None:
            e = VesaliusWSException(data_dict)
            raise HTTPException(status_code=400, detail=e.message)
        
        s = data_dict.get('Result').get('Token').get('Token_number')
        return s.strip()
    
    async def logout(self, token_number: str):
        cli = self.__getClient('AUTHENTICATION/Logout.cfc')
        result = await cli.service.Logout(token_number)
        res = self.__parseXML(result)
        data_dict = xmltodict.parse(res)
        if data_dict.get('Result') is not None and data_dict.get('Result').get('Error') is not None:
            e = VesaliusWSException(data_dict)
            raise HTTPException(status_code=400, detail=e.message)
        
        return data_dict
    
    async def patientGetPatientData(self, prn: str):
        result = await self.__patientGetPatientDataRes(prn)
        if result is not None:
            res = self.__parseXML(result)
            data_dict = xmltodict.parse(res)
            if data_dict.get('Result') is not None and data_dict.get('Result').get('Error') is not None:
                e = VesaliusWSException(data_dict)
                if e.code == 'WS-00014':
                    raise HTTPException(status_code=400, detail='The Identification Number provided does not exist in our hospital records. Please retry.')
                
                raise HTTPException(status_code=400, detail="Error encountered. Please contact Island Hospital. (Error Code: f'{e.code}')")
            
            else:
                return Patient.fromDict(data_dict)
        
        return None
    
    async def __patientGetPatientDataRes(self,  prn: str) -> str:
        cli = self.__getClient('PATIENT/GetPatientData.cfc')
        return await cli.service.getPatientData(prn)
        
    def __parseXML(self, s: str):
        return s.replace('encoding="UTF-8">', 'encoding="UTF-8"?>')
    
    def __getClient(self, s: str) -> AsyncClient:
        opt = Settings(strict=False)
        baseUrl = settings.vesaliusServerBaseUrl
        wsdl = f'{baseUrl}{s}?wsdl'
        client = AsyncClient(wsdl, settings=opt)
        return client