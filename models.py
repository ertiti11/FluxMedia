from pydantic import BaseModel
from typing import List, Dict, Optional

class UserIdentity(BaseModel):
    principalId: str

class RequestParameters(BaseModel):
    principalId: str
    region: str
    sourceIPAddress: str

class ResponseElements(BaseModel):
    x_amz_id_2: str
    x_amz_request_id: str
    x_minio_deployment_id: str
    x_minio_origin_endpoint: str

class Bucket(BaseModel):
    name: str
    ownerIdentity: UserIdentity
    arn: str

class ObjectData(BaseModel):
    key: str
    size: int
    eTag: str
    contentType: str
    userMetadata: Dict[str, str]
    sequencer: str

class S3(BaseModel):
    s3SchemaVersion: str
    configurationId: str
    bucket: Bucket
    object: ObjectData

class Source(BaseModel):
    host: str
    port: Optional[str]
    userAgent: str

class Record(BaseModel):
    eventVersion: str
    eventSource: str
    awsRegion: str
    eventTime: str
    eventName: str
    userIdentity: UserIdentity
    requestParameters: RequestParameters
    responseElements: ResponseElements
    s3: S3
    source: Source

class WebhookPayload(BaseModel):
    EventName: str
    Key: str
    Records: List[Record]