from dataclasses import dataclass, field
from typing import List, Union

def toStr(o):
    return str(o) if o is not None else o

@dataclass
class VesaliusWSException:
    code: str
    message: str
    
    def __init__(self, dic: dict):
        e = dic.get('Result').get('Error')
        self.code = e.get('ErrorCode')
        self.message = e.get('ErrorMessage')

@dataclass         
class Document:
    code: str
    description: str
    value: Union[str, None] = None
    expireDate: Union[str, None] = None
    
    def __init__(self, dic: dict):
        self.code = toStr(dic.get('Code'))
        self.description = toStr(dic.get('Description'))
        self.value = toStr(dic.get('Value'))
        self.expireDate = toStr(dic.get('ExpireDate'))
  
@dataclass      
class Nationality:
    code: str
    description: str
    
    def __init__(self, dic: dict):
        self.code = toStr(dic.get('Code'))
        self.description = toStr(dic.get('Description'))
 
@dataclass       
class Sex(Nationality):
    code: str
    description: str
    
    def __init__(self, dic: dict):
        super().__init__(dic)

@dataclass        
class Address:
    address1: str
    address2: Union[str, None] = None
    address3: Union[str, None] = None
    cityState: Union[str, None] = None
    postalCode: Union[str, None] = None
    country: Union[str, None] = None
    
    def __init__(self, dic: dict):
        self.address1 = toStr(dic.get('Address1'))
        self.address2 = toStr(dic.get('Address2'))
        self.address3 = toStr(dic.get('Address3'))
        self.cityState = toStr(dic.get('CityState'))
        self.postalCode = toStr(dic.get('PostalCode'))
        self.country = toStr(dic.get('Country'))
  
@dataclass      
class ContactNumber:
    home: Union[str, None] = None
    email: Union[str, None] = None
    
    def __init__(self, dic: dict):
        self.home = toStr(dic.get('Home'))
        self.email = toStr(dic.get('Email'))
 
@dataclass       
class Name:
    title: str
    firstName: str
    middleName: Union[str, None] = None
    lastName: Union[str, None] = None
    
    def __init__(self, dic: dict):
        self.title = toStr(dic.get('Title'))
        self.firstName = toStr(dic.get('FirstName'))
        self.middleName = toStr(dic.get('MiddleName'))
        self.lastName = toStr(dic.get('LastName'))
        
@dataclass
class Patient:
    prn: str
    name: str
    resident: Union[str, None] = None
    dob: Union[str, None] = None
    contactNumber: Union[ContactNumber, None] = None
    homeAddress: Union[Address, None] = None
    sex: Union[Sex, None] = None
    documents: List[Document] = field(default_factory=list)
    nationality: Union[Nationality, None] = None
    
    def __init__(self, dic: dict):
        xDocument: list[Document] = []
        dx = dic.get('Document')
        if isinstance(dx, list):
            for k in dx:
                xDocument.append(Document(k))
            
        else:
            if 'Document' in dic:
                xDocument = [Document(dx)]
            
        self.prn = toStr(dic.get('PRN'))
        self.name = Name(dic.get('Name'))
        self.resident = toStr(dic.get('Resident'))
        self.dob = toStr(dic.get('DOB'))
        self.contactNumber = ContactNumber(dic.get('ContactNumber'))
        self.homeAddress = Address(dic.get('HomeAddress'))
        self.sex = Sex(dic.get('Sex'))
        self.documents = xDocument
        self.nationality = Nationality(dic.get('Nationality'))
        
    @classmethod
    def fromDict(cls, dic: dict):
        x = dic.get('Result').get('Patient')
        if isinstance(x, list):
            return cls.dictToList(x)
        
        return Patient(x)
        
    @classmethod
    def dictToList(cls, dic: dict):
        lx: list[Patient] = []
        for k in dic:
            lx.append(Patient(k))
            
        return lx