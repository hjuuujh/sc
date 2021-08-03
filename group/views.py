from django.shortcuts import render, redirect
from django.views import generic
from group.forms import GroupForm
from django.utils import timezone
from group.models import Group, Join
from board.models import Board
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User


# Create your views here.
class IndexView(generic.ListView):    #그룹 전체 리스트
    paginate_by = 10
    template_name = "group/group_list.html"
    context_object_name = 'group_list'

    def get_queryset(self):
        group_list =  Group.objects.filter(
            id__in=Join.objects.filter(uid=self.request.user)
                .order_by('date')
                .values('gid')
        )
        return group_list


def group_page(request, pk):
    board = Board.objects.filter(gid=pk)
    return redirect('board:post_list', group_id=pk, pk=board[0].id)

def Index(request):                       # 그룹 검색 페이지 함수

    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    search_list = Group.objects.all().order_by('name')

    if kw:
        search_list = search_list.filter(
            Q(name__icontains=kw) |
            Q(goal__icontains=kw) |
            Q(info__icontains=kw)
        ).distinct()

    paginator = Paginator(search_list, 10)
    page_obj = paginator.get_page(page)

    context = {'search_list': page_obj, 'page': page, 'kw': kw}
    print(search_list)

    return render(request, 'group/search_list.html', context)


class DetailView(generic.DetailView):             #그룹 상세보기
    model = Group


@login_required(login_url='common:login')
def group_create(request):                            # 그룹 생성
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.uid = request.user
            group.members = 1
            group.date = timezone.now()
            group.save()
            return redirect('group:group_list')
    else:
        groupform = GroupForm()
        context = {'form': groupform}
    return render(request, 'group/group_form.html', context)


# def join_group(request):
#     my_form = JoinForm()
#     if request.method == 'POST':
#         join = my_form.save(commit=False)
#         # join.uid = request.user  
#         # join.members += 1
#         join.join_date = timezone.now()
#         join.save()
#         return redirect('group:group_list')
#     else:
#         my_form = JoinForm()
#         context = {'form': my_form}
#         return render(request, 'group/group_detail.html', context) 


@login_required(login_url='common:login')
def join_group(request, pk):
    join = Join()
    join.uid_id = request.user.id
    join.gid_id = pk
    join.date = timezone.now()
    join.save()

    selected_group = Group.objects.get(id=pk)
    selected_group.members += 1
    selected_group.save()
    return redirect('group:group_list')


