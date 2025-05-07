from ninja import Router

router = Router()


@router.get("/")
def barks_list(request):
    """
    Bark list endpoint that returns a list of barks.
    """
    return [{'id':1, 'message': 'bark 1!'}, {'id':2, 'message': 'bark 2!'}, {'id':3, 'message': 'bark 3!'}]


@router.get("/{bark_id}/")
def get_bark(request, bark_id: int):
    """
    Bark detail endpoint that returns a single bark.
    """
    return {"id": bark_id, "message": f"bark {bark_id}!"}
