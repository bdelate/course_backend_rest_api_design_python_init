from ninja import Router

router = Router()


@router.get("/")
def barks_list(request):
    """
    Bark list endpoint that returns a list of barks.
    """
    return [{'id':1, 'message': 'bark one!'}, {'id':2, 'message': 'bark two!'}, {'id':3, 'message': 'bark three!'}]
