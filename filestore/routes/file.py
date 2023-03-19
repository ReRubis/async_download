from fastapi import APIRouter, Depends, File, HTTPException, status
from fastapi.responses import FileResponse

from filestore.services.file_service import FileAppService


router = APIRouter(
    prefix='/file',
    tags=['file work'],
    # dependencies=[]
)


@router.get('/{id}', response_class=FileResponse)
async def get_file(
    id,
    service: FileAppService = Depends(FileAppService)
):
    """Get a file with specified id"""
    file_location = service.store_service.get(id)
    return file_location


@router.get('/', response_class=FileResponse)
async def get_files(
    service: FileAppService = Depends(FileAppService)
):
    """Get a list of files"""
    ...


@router.post('/')
async def upload_file_by_link(
    service: FileAppService = Depends(FileAppService)
):
    """Make the service download a file from a given link"""
    ...


@router.post('/upload')
async def upload(
    service: FileAppService = Depends(FileAppService)
):
    """Upload file"""
    ...


@router.delete('/{id}')
async def delete_file(
    service: FileAppService = Depends(FileAppService)
):
    """Deletes file with a specified id"""
    ...