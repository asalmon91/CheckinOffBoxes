from collections import defaultdict

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, DetailView, CreateView, DeleteView

from board.models import Board, TaskState, Task, TaskForm, BoardForm


class COBSignupView(CreateView):
    form_class = UserCreationForm
    success_url = '/'  # login?
    template_name = 'board/signup.html'


class COBLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'board/login.html'


class COBLogoutView(LogoutView):
    pass


def create_example_board(request):
    board_model_manager = Board.objects
    task_state_model_manager = TaskState.objects
    task_model_manager = Task.objects

    board_name = "My First Board"
    if not board_model_manager.filter(name=board_name).exists():
        board_model_manager.create(name=board_name)
    test_board = board_model_manager.filter(name=board_name).first()

    task_states = ["TODO", "In Progress", "Done"]
    for i in range(len(task_states)):
        if not task_state_model_manager.filter(board=test_board, name=task_states[i]).exists():
            task_state_model_manager.create(board=test_board, name=task_states[i], index=i)
    todo_task_state = task_state_model_manager.filter(name="TODO").first()

    # TODO: This is going to create a new task if you ever update the initial task
    task_name = "Learn Django"
    if not task_model_manager.filter(name=task_name, task_state=todo_task_state).exists():
        task_model_manager.create(
            task_state=todo_task_state,
            name=task_name
        )

    t = task_model_manager.filter(name=task_name, task_state=todo_task_state).first()
    assert isinstance(t, Task)
    response = t.name
    return HttpResponse(response)


class MainView(View):

    def get(self, request, *args, **kwargs):
        return redirect('boards/')


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'board/board_set.html'

    def get_queryset(self):
        return super().get_queryset().annotate(
            task_count=Count('task_states__tasks', distinct=True)
        )


class BoardView(DetailView):
    model = Board
    template_name = 'board/board.html'


class BoardFormView(FormView):
    form_class = BoardForm
    template_name = "board/board_form.html"
    success_url = "/boards/"
    initial = {
        'name': '',
        'description': ''
    }

    board_list = defaultdict(list)

    def get(self, request, *args, **kwargs):
        if kwargs:
            board = Board.objects.filter(id=kwargs['pk']).first()
            form = self.form_class(initial={
                'name': board.name,
                'description': board.description
            })
        else:
            form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        author = 'Anonymous'
        if request.user.is_authenticated:
            author = request.user.username
        form = self.form_class(request.POST)
        if form.is_valid():
            board_data = form.cleaned_data
            if kwargs:
                board = Board.objects.filter(id=kwargs['pk']).first()
                board.name = board_data['name']
                board.description = board_data['description']
            else:
                board = Board(**board_data)
            board.save()
            return redirect('/boards/')
        return None

    def delete(self, request, board, *args, **kwargs):
        author = 'Anonymous'
        if request.user.is_authenticated:
            author = request.user.username

        if board in self.board_list[author]:
            self.board_list[author].remove(board)
        else:
            raise Http404
        return redirect('/')


class BoardDeleteView(DeleteView):
    model = Board
    template_name = "board/board_confirm_delete.html"
    success_url = reverse_lazy("board-set")


class TaskFormView(FormView):
    form_class = TaskForm
    template_name = "board/task_form.html"
    success_url = "/board/task"
