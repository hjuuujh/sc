from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from group.forms import GroupForm
from django.utils import timezone
from group.models import Group, Join, JoinRequest
from board.models import Board
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages


# Create your views here.
class IndexView(generic.ListView):  # 그룹 전체 리스트
    paginate_by = 10
    template_name = "group/group_list.html"
    context_object_name = 'group_list'

    def get_queryset(self):
        group_list = Group.objects.filter(
            id__in=Join.objects.filter(uid=self.request.user)
                .values('gid')
                .order_by('date')
        )
        return group_list


def group_page(request, pk):
    board = Board.objects.filter(gid=pk).first()
    return redirect('board:post_list', group_id=pk, pk=board.id)


def index(request):  # 그룹 검색 페이지 함수

    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    # search_list = Group.objects.all().order_by('name')
    type = request.GET.get('type', '')
    so = request.GET.get('so', 'recent')  # 정렬기준

    if so == 'member':
        search_list = Group.objects.order_by('-members')
    else:  # recent
        search_list = Group.objects.order_by('-date')

    # 검색
    if kw:
        if type == 'all':
            search_list = search_list.filter(
                Q(name__icontains=kw) |
                Q(goal__icontains=kw) |
                Q(info__icontains=kw)
            ).distinct()
        elif type == 'name':
            search_list = search_list.filter(
                Q(name__icontains=kw)
            ).distinct()
        elif type == 'goal':
            search_list = search_list.filter(
                Q(goal__icontains=kw)
            ).distinct()
        elif type == 'info':
            search_list = search_list.filter(
                Q(info__icontains=kw)
            ).distinct()

    paginator = Paginator(search_list, 10)
    page_obj = paginator.get_page(page)

    context = {'search_list': page_obj, 'page': page, 'kw': kw, 'so': so}

    return render(request, 'group/search_list.html', context)


class DetailView(generic.DetailView):  # 그룹 상세보기
    model = Group


@login_required(login_url='common:login')
def group_create(request):  # 그룹 생성
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.uid_id = request.user.id
            group.members = 0
            group.date = timezone.now()
            group.save()

            board = Board()
            board.bname = "Study"
            board.gid_id = group.id
            board.create_date = timezone.now()
            board.save()

            approve_request(request, request.user.id,group.id,1)
            return redirect('group:group_list')
    else:
        groupform = GroupForm()
        context = {'form': groupform}
    return render(request, 'group/group_form.html', context)


class GroupCreateView(generic.ListView):
    template_name = "group/group_mgr.html"
    context_object_name = 'group_create_list'
    paginate_by = 10

    def get_queryset(self):
        group_create_list = Group.objects.filter(uid=self.request.user)
        return group_create_list


def group_delete(request, pk):
    group = get_object_or_404(Group, id=pk)
    group.delete()
    return redirect('group:group_list')


class GroupJoinView(generic.ListView):
    model = Group
    template_name = "group/group_join.html"
    context_object_name = 'group_join_list'
    paginate_by = 10

    def get_queryset(self):
        group_join_list = Group.objects.filter(
            id__in=Join.objects.filter(uid=self.request.user)
                .order_by('date')
                .values('gid')
        ).exclude(uid=self.request.user)
        return group_join_list


def group_leave(request, group_id):
    join = get_object_or_404(Join, uid=request.user.id, gid=group_id)
    join.delete()

    group = get_object_or_404(Group, id=group_id)
    group.members -= 1
    group.save()
    return redirect('group:group_list')

def join_request(request, group_id):
    motivation = request.GET.get('motivation')

    selected_group = Group.objects.get(id=group_id)
    joined = Join.objects.filter(uid_id=request.user.id, gid_id=group_id)
    if selected_group.members == selected_group.max_members:
        messages.warning(request, "가입 인원이 마감되어 가입이 불가합니다.")
        return redirect('group:group_detail', pk=group_id)
    elif (joined):
        messages.warning(request, "이미 가입한 그룹입니다.")
        return redirect('group:group_detail', pk=group_id)
    else:
        try:
            group_join_request = JoinRequest()
            group_join_request.uid_id = request.user.id
            group_join_request.gid_id = group_id
            group_join_request.motivation = motivation
            group_join_request.date = timezone.now()
            group_join_request.save()

            return redirect('group:group_join_request')

        except IntegrityError as e:
            if 'UNIQUE constraint' in e.args[0]:
                messages.warning(request, "가입 승인 대기중인 그룹입니다.")
                return redirect('group:group_detail', pk=group_id)
    return redirect('group:group_join_request')

class GroupJoinRequestView(generic.ListView):
    model = JoinRequest
    template_name = "group/group_request.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_request_list'] = JoinRequest.objects.filter(gid__in = Group.objects.filter(uid = self.request.user).values('id'))
        context['group_apply_list'] = JoinRequest.objects.filter(uid = self.request.user)
        return context

def approve_request(request, user_id, group_id, approve):
    request_approve = JoinRequest.objects.filter(uid_id=user_id, gid_id=group_id)
    request_approve.delete()

    if(approve):
        join = Join()
        join.uid_id = user_id
        join.gid_id = group_id
        join.date = timezone.now()
        join.save()

        selected_group = Group.objects.get(id=group_id)
        selected_group.members += 1
        selected_group.save()

    return redirect('group:group_join_request')



