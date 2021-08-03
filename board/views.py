from django.shortcuts import render , get_object_or_404, redirect

from django.utils import timezone
from django.views import generic
from board.models import Board, Post, Comment
from group.models import Group, Join
from django.contrib.auth.decorators import login_required
from board.forms import PostForm, CommentForm, BoardForm
from django.contrib.auth.models import User
from itertools import chain

class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_detail'] = Post.objects.get(id=self.kwargs['pk'])
        context['group'] = Group.objects.get(id = self.kwargs['group_id'])

        return context

class PostListView(generic.ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = Group.objects.get(id=self.kwargs['group_id'])
        context['board_list'] = Board.objects.filter(gid_id= self.kwargs['group_id'])
        context['post_list'] = Post.objects.filter(bid_id=self.kwargs['pk'])
        context['bid'] = self.kwargs['pk']

        return context


@login_required(login_url='common:login')
def post_create(request, group_id ,board_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.gid_id = group_id
            post.bid_id = board_id
            post.uid_id = request.user.id
            post.create_date = timezone.now()
            post.save()

            return redirect('board:post_detail', group_id=group_id, board_id=board_id,pk=post.id)
    else:
        form = PostForm()
        context = {'form': form, 'group': Group.objects.get(id=group_id)}

        return render(request, 'board/post_form.html', context)


# 게시글 수정 / 삭제

@login_required(login_url='common:login')
def post_modify(request, board_id, pk):

    post = get_object_or_404(Post, pk=pk)
    if request.user != post.uid:
        print("post.uid:", post.uid)
        print("request.user", request.user)
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:post_detail', group_id=post.gid.id, board_id=board_id, pk=post.id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.bid_id = board_id
            post.create_date = timezone.now()  # 수정일시 저장
            post.save()
            return redirect('board:post_detail', group_id=post.gid.id, board_id=board_id, pk=post.id)

    else:
        form = PostForm(instance=post)
        context = {'form': form, 'group': Group.objects.get(id=post.gid.id)}
    return render(request, 'board/post_form.html', context)


# @login_required(login_url='common:login')
def post_delete(request, group_id, board_id, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.uid:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board:post_detail', group_id=group_id, board_id=board_id, pk=post.id)
    post.delete()
    return redirect('board:post_list', group_id=group_id, pk = board_id)


@login_required(login_url='common:login')
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.uid_id = request.user.id
            comment.pid_id = post_id
            comment.create_date = timezone.now()
            comment.save()
            return redirect('board:post_detail', group_id=post.gid.id, board_id=post.bid.id, pk=post.id)

    else:
        form = CommentForm()
    context = {'form': form, 'group': Group.objects.get(id=post.gid.id)}
    return render(request, 'board/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk= comment_id)

    if request.user != comment.uid:
        print("comment.uid:", comment.uid)
        print("request.user", request.user)
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:post_detail', comment_id=comment_id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.create_date = timezone.now()  # 수정일시 저장
            comment.save()
            return redirect('board:post_detail', group_id=comment.pid.gid.id, board_id=comment.pid.bid.id,pk=comment.pid.id)
    else:
        form = CommentForm(instance=comment)
    context = {'comment': comment , 'form': form , 'group': Group.objects.get(id=comment.pid.gid.id)}
    return render(request, 'board/comment_form.html', context)


def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    print(request.user)
    if request.user != comment.uid:
        messages.error(request, '삭제권한이 없습니다')
    else:
        comment.delete()

    return redirect('board:post_detail', group_id=comment.pid.gid.id, board_id=comment.pid.bid.id, pk=comment.pid.id)


class BoardListView(generic.ListView):
    model = Board

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board_list'] = Board.objects.filter(gid_id=self.kwargs['pk'])
        context['gid'] = self.kwargs['pk']
        return context


def board_create(request, group_id):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.gid_id = group_id
            board.create_date = timezone.now()
            board.save()
            return redirect('board:board_list', pk=group_id)
    else:
        form = BoardForm()
        context = {'form': form}
        return render(request, 'board/board_form.html', context)


def board_delete(request, group_id, pk):
    board = get_object_or_404(Board, pk=pk)
    board.delete()
    return redirect('board:board_list', pk = group_id)


def group_leave(request, group_id):
    join = get_object_or_404(Join, uid = request.user.id, gid = group_id)
    join.delete()

    group = get_object_or_404(Group, id = group_id)
    group.members -= 1
    group.save()
    return redirect('group:group_list', pk = request.user.id)

