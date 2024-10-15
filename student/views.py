from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from student.models import Assignment, Submission, MyUser
from student.forms import SignupForm, SigninForm, AssignmentForm, SubmissionForm

def signup(request):
    if request.user.is_authenticated:
         messages.info(request, "User already logged in")
         return redirect("student:base")
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            value = form.save(commit=False)
            if request.POST.get('choice')=='student':
                value.student=True
                value.teacher=False
            else:
                value.student = False
                value.teacher = True
            value.save()
            messages.success(request, "User created successfully")
            return redirect("student:signin")
        else:
            messages.info(request, "Invalid form")
    else:
        form = SignupForm()
    return render(request, "student/signup.html", {"form": form})

def signin(request):
    if request.user.is_authenticated:
        messages.info(request, "User already logged in")
        return redirect("student:base")
    if request.method == "POST":
        form = SigninForm(request.POST)
        username = form["username"].value() # req.POST.get('username')
        password = form["password"].value()
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
        else:
            messages.error(request, "Invalid Username or Password")

        if user.student == True:
            return redirect('student:base')
        else:
            creation = AssignmentForm()
            return redirect('student:base')
    else:
        form = SigninForm()
    return render(request, "student/signin.html", {"form":form})


@login_required(login_url='/signin')
def create_assignment(request):
    if request.user.teacher:  # Ensure only teachers can access this view
        if request.method == "POST":
            form = AssignmentForm(request.POST, request.FILES or None)
            if form.is_valid():
                assignment = form.save(commit=False)
                assignment.user = request.user
                assignment.save()
                messages.success(request, "Assignment created successfully")
                return redirect("student:base")  # Redirect after success
            else:
                messages.error(request, "Form is invalid. Please correct the errors below.")
        else:
            form = AssignmentForm()  # If not a POST request, initialize an empty form

        # In case of GET request or form errors, render the teacher page with the form
        profile = MyUser.objects.get(id=request.user.id)
        return render(request, "student/teacher.html", {"form": form, 'profile': profile})

    else:
        raise Http404("You are not authorized to create assignments.")


@login_required(login_url='/signin')
def assignment_submission(request):
    if request.user.student == True:
        if request.method == "POST":
            form = SubmissionForm(request.POST or None,request.FILES)
            if form.is_valid():
                value = form.save(commit=False)
                value.user_id = request.user.id
                value.save()
                messages.success(request,"Assignment submitted successfully")
                return redirect("student:student_submitted",)

            else:
                messages.info(request, "form is invalid")
                form = SubmissionForm()
                return render(request, "student/students.html", {"form": form})
        else:
            form = SubmissionForm()
            profile = MyUser.objects.get(id=request.user.id)
            return render(request, "student/students.html", {"form": form,'profile':profile})
    else:
        raise Http404
def submit_button(request,id):
    if request.user.student == True:
        if request.method == "POST":
            form = SubmissionForm(request.POST or None,request.FILES)
            if form.is_valid():
                value = form.save(commit=False)
                value.user_id = request.user.id
                value.save()
                messages.success(request,"Assignment submitted successfully")
                return redirect("student:student_submitted",)

            else:
                messages.info(request, "form is invalid")
                form = SubmissionForm()
                return render(request, "student/students.html", {"form": form})
        else:
            form = SubmissionForm()
            profile = MyUser.objects.get(id=request.user.id)
            return render(request, "student/students.html", {"form": form,'profile':profile})
    else:
        raise Http404
@login_required(login_url='/signin')
def signout(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("student:signin")

def delete_assignment(request, id=None):
    if request.user.is_authenticated:
        instance = get_object_or_404(Assignment,id=id)
        instance.delete()
        messages.success(request,'post deleted')
        return redirect("student:base")
    else:
        messages.info(request, "You need to be authenticated to perform this operation.")
        return redirect("student:signin")

def edit_assignment(request,id=None):
    if request.user.is_authenticated:
        instance = Assignment.objects.get(id=id)
        aform = AssignmentForm(request.POST or None, request.FILES or None,instance=instance)
        context = {
            'form': aform,
        }
        if aform.is_valid():
            instance = aform.save(commit=False)
            instance.save()
            messages.success(request, 'Assignment was successfully edited.')
            return redirect('student:base')

    else:
        messages.info(request, "You need to be authenticated to perform this operation.")
    return render(request, "student/teacher.html", context)

def submitted(request,id):
        if request.user.is_authenticated:
            submissions = Submission.objects.filter(assignment_id=id)
            data = {"submit": submissions, }
            return render(request, "student/submission.html", data)
        else:
            messages.info(request, "You need to login to view the submitted page.")
            return redirect("student:signin")

def student_submitted(request):
    if request.user.is_authenticated:
        submissions = Submission.objects.filter(active=True)
        data = {"submit": submissions, }
        return render(request, "student/submission.html", data)
    else:
        messages.info(request, "You need to login to view the submitted page.")
        return redirect("student:signin")

def base(request):
        assignments = Assignment.objects.filter(active=True)
        submissions = Submission.objects.filter(active=True)
        profile = MyUser.objects.get(id=request.user.id)
        context = {"context": assignments,"submit": submissions, "profile": profile}
        return render(request, 'student/base.html', context)

class Assignmentsubmit(DetailView):
    model = Submission
    template_name = 'student/detail.html'

