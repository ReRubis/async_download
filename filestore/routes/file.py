from fastapi import APIRouter, Depends, File, HTTPException, status
from fastapi.responses import FileResponse

router = APIRouter(
    prefix='/file',
    tags=['work with files']
)


@router.get('/{id}')
async def get_file():
    """Get a file with specified id"""
    return FileResponse()


@router.get('/')
async def get_files():
    """Get a list of files"""
    ...


@router.post('/')
async def upload_file_by_link():
    """Make the service download a file from a given link"""
    ...


@router.post('/upload')
async def upload():
    """Upload file"""
    ...


@router.delete('/{id}')
async def delete_file():
    """Deletes file with a specified id"""
    ...
