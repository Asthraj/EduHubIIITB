from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Assignment

def assignment_list(request):
    assignments = Assignment.objects.all()

    for assignment in assignments:
        assignment.is_submitted = assignment.submission_set.filter(
            student=request.user
        ).exists()

    return render(request, 'classroom/assignment_list.html', {
        'assignments': assignments
    })