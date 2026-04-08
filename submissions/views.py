from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from classroom.models import Assignment
from .forms import SubmissionForm
from django.contrib.auth.decorators import login_required

from django.utils import timezone

@login_required
def submit_assignment(request, id):

    # Role check
    if request.user.role != 'student':
        return redirect('dashboard')

    assignment = get_object_or_404(Assignment, id=id)

    # ✅ ADD DEADLINE CHECK HERE
    if timezone.now() > assignment.deadline:
        return render(request, 'submissions/submit.html', {
            'form': None,
            'assignment': assignment,
            'error': 'Deadline passed'
        })

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect('dashboard')
    else:
        form = SubmissionForm()

    return render(request, 'submissions/submit.html', {
        'form': form,
        'assignment': assignment
    })


from .models import Submission
from django.contrib.auth.decorators import login_required


@login_required
def teacher_submissions(request):
    # ✅ Only teacher allowed
    if request.user.role != 'teacher':
        return redirect('dashboard')

    submissions = Submission.objects.all().order_by('-submitted_at')

    return render(request, 'submissions/teacher_submissions.html', {
        'submissions': submissions
    })
from .forms import GradeForm
from django.shortcuts import get_object_or_404

@login_required
def grade_submission(request, id):

    # ✅ Only teacher allowed
    if request.user.role != 'teacher':
        return redirect('dashboard')

    submission = get_object_or_404(Submission, id=id)

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('teacher_submissions')
    else:
        form = GradeForm(instance=submission)

    return render(request, 'submissions/grade.html', {
        'form': form,
        'submission': submission
    })