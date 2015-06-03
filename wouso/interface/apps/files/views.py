from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.decorators import permission_required

from wouso.core.ui import register_sidebar_block
from wouso.interface.apps.files.models import FileCategory, File


@permission_required('files.can_list_files')
def index(request):
    """ Shows all lessons related to the current user """

    categories = FileCategory.objects.all()

    return render_to_response('files/index.html',
                              {'categories': categories},
                              context_instance=RequestContext(request))


def sidebar_widget(context):
    user = context.get('user', None)
    if not user or not user.is_authenticated():
        return ''

    if File.disabled():
        return ''

    number_of_files = File.objects.all().count()
    return render_to_string('files/sidebar.html',
            {'number_of_files': number_of_files})


register_sidebar_block('files', sidebar_widget)
