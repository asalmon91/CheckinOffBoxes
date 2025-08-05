from collections import defaultdict

from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView, ListView, DetailView

from board.models import Board, TaskState, Task, TaskForm, BoardForm


# Create your views here.
def example_view(request):
    return HttpResponse("Hello, world")


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
        # context = {'user_name': 'Alex'}
        return redirect('boards/')


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'board/board_set.html'


class BoardView(DetailView):
    model = Board
    template_name = 'board/board.html'


class BoardFormView(FormView):
    form_class = BoardForm
    template_name = "board/board_form.html"
    success_url = "/boards/board"
    initial = {
        'name': '',
        'description': ''
    }

    board_list = defaultdict(list)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        author = 'Anonymous'
        if request.user.is_authenticated:
            author = request.user.username
        form = self.form_class(request.POST)
        if form.is_valid():
            board = form.cleaned_data['board']
            self.board_list[author].append(board)
            return redirect('/')
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


class TaskFormView(FormView):
    form_class = TaskForm
    template_name = "board/task_form.html"
    success_url = "/board/task"
