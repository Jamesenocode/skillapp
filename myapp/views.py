from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Count
from openpyxl import Workbook

from .models import TrainingApplication, AdminActivityLog
from .forms import TrainingApplicationForm, StudentRegistrationForm

# Helper function to check if a user is staff
def is_admin(user):
    return user.is_staff

# --- Public Views ---

def myfunctioncall(request):
    return HttpResponse("Welcome") 

def myfirstpage(request):
    return render(request, 'index.html')

def about(request):
    return render(request, "myapp/about.html")

def home(request):
    # Enforce strict routing for logged-in sessions to custom dashboards
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin_dashboard")
        return redirect("student_dashboard")

    programs = [
        "ICT",
        "Computer for Beginners",
        "Computer Graphics",
        "Plumbing",
        "Alamaco & Aluminium Works",
        "Electrical Electronics",
        "Solar System Installation",
    ]

    return render(request, "myapp/home.html", {
        "programs": programs,
    })

def programs(request):
    program_list = [
        {
            "name": "ICT",
            "description": "Computer for Beginners and basic digital skills training.",
            "duration": "5th June - 15th June, 2026",
        },
        {
            "name": "Computer Graphics",
            "description": "Design training for posters, branding, and visual communication.",
            "duration": "5th June - 15th June, 2026",
        },
        {
            "name": "Plumbing",
            "description": "Piping, fittings, installation, and practical repair skills.",
            "duration": "5th June - 15th June, 2026",
        },
        {
            "name": "Electrical Electronics",
            "description": "Hands-on electrical and electronics training.",
            "duration": "5th June - 15th June, 2026",
        },
        {
            "name": "Solar System Installation",
            "description": "Solar panel installation, setup, and maintenance basics.",
            "duration": "5th June - 15th June, 2026",
        },
        {
            "name": "Alamaco & Aluminium Works",
            "description": "Practical aluminium fabrication and installation training.",
            "duration": "5th June - 15th June, 2026",
        },
    ]

    return render(request, "myapp/programs.html", {
        "programs": program_list,
    })

@login_required
def check_status(request):
    application = None
    message = None

    if request.method == "POST":
        phone_number = request.POST.get("phone_number")

        try:
            application = TrainingApplication.objects.filter(
                phone_number=phone_number
            ).latest("application_date")
        except TrainingApplication.DoesNotExist:
            message = "No application was found with that phone number."

    return render(request, "myapp/check_status.html", {
        "application": application,
        "message": message,
    })


# --- Authentication Views ---

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            messages.info(request, "An account with this email already exists. Please login.")
            return redirect("student_login")

        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            user = User.objects.create_user(
                username=email,
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=email,
                password=form.cleaned_data["password"],
            )

            login(request, user)
            return redirect("student_dashboard")
    else:
        form = StudentRegistrationForm()

    return render(request, "myapp/register.html", {
        "form": form,
    })

def student_login(request):
    if request.method == "POST":
        identifier = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=identifier, password=password)

        if user is None:
            try:
                found_user = User.objects.get(email=identifier)
                user = authenticate(request, username=found_user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect("admin_dashboard")

            return redirect("student_dashboard")

        return redirect("register")

    return render(request, "myapp/login.html")

def student_logout(request):
    logout(request)
    return redirect("home")


# --- Student Dashboard & Application Views ---

@login_required
def student_dashboard(request):
    application = TrainingApplication.objects.filter(
        student=request.user
    ).order_by("-application_date").first()

    return render(request, "myapp/student_dashboard.html", {
        "application": application,
    })

@login_required
def apply(request):
    existing_application = TrainingApplication.objects.filter(
        student=request.user
    ).order_by("-application_date").first()

    if existing_application:
        return redirect("student_dashboard")

    if request.method == "POST":
        form = TrainingApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user

            # Automatically set Category tracking based on age boundaries
            if application.age <= 17:
                application.category = "Children"
            else:
                application.category = "Adult"

            application.save()
            return redirect("application_success")
    else:
        form = TrainingApplicationForm()

    return render(request, "myapp/apply.html", {
        "form": form,
    })

def application_success(request):
    return render(request, "myapp/application_success.html")


# --- Admin Views ---

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_applications = TrainingApplication.objects.count()
    pending_applications = TrainingApplication.objects.filter(status="Pending").count()
    approved_applications = TrainingApplication.objects.filter(status="Approved").count()
    rejected_applications = TrainingApplication.objects.filter(status="Rejected").count()

    recent_applications = TrainingApplication.objects.order_by("-application_date")[:5]

    program_statistics = (
        TrainingApplication.objects
        .values("program")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    return render(request, "myapp/admin_dashboard.html", {
        "total_applications": total_applications,
        "pending_applications": pending_applications,
        "approved_applications": approved_applications,
        "rejected_applications": rejected_applications,
        "recent_applications": recent_applications,
        "program_statistics": program_statistics,
    })

@login_required
@user_passes_test(is_admin)
def admin_applications(request):
    applications = TrainingApplication.objects.order_by("-application_date")

    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")
    program_filter = request.GET.get("program", "")

    if search_query:
        applications = applications.filter(
            Q(surname__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(middle_name__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    if status_filter:
        applications = applications.filter(status=status_filter)

    if program_filter:
        applications = applications.filter(program=program_filter)

    return render(request, "myapp/admin_applications.html", {
        "applications": applications,
        "search_query": search_query,
        "status_filter": status_filter,
        "program_filter": program_filter,
        "status_choices": TrainingApplication.STATUS_CHOICES,
        "program_choices": TrainingApplication.PROGRAM_CHOICES,
    })

@login_required
@user_passes_test(is_admin)
def admin_application_detail(request, application_id):
    application = get_object_or_404(TrainingApplication, id=application_id)

    if request.method == "POST":
        status = request.POST.get("status")
        admin_message = request.POST.get("admin_message")

        if status in ["Pending", "Approved", "Rejected"]:
            application.status = status
            application.admin_message = admin_message
            application.reviewed_at = timezone.now()
            application.save()

            return redirect("admin_applications")

    return render(request, "myapp/admin_application_detail.html", {
        "application": application,
    })

@login_required
@user_passes_test(is_admin)
def admin_export_excel(request):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Applications"

    headers = [
        "Surname", "First Name", "Middle Name", "Phone", "Program",
        "Duration", "Category", "Status", "Admin Message", "Submitted"
    ]
    sheet.append(headers)

    applications = TrainingApplication.objects.order_by("-application_date")

    for app in applications:
        sheet.append([
            app.surname,
            app.first_name,
            app.middle_name,
            app.phone_number,
            app.program,
            app.duration,
            app.category,
            app.status,
            app.admin_message,
            app.application_date.strftime("%Y-%m-%d %H:%M"),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="karo_applications.xlsx"'

    workbook.save(response)
    return response

@login_required
@user_passes_test(is_admin)
def admin_bulk_action(request):
    if request.method == "POST":
        application_ids = request.POST.getlist("application_ids")
        action = request.POST.get("bulk_action")

        if application_ids and action:
            applications = TrainingApplication.objects.filter(id__in=application_ids)

            # Bulk Delete processing logic
            if action == "Delete":
                count = applications.count()
                applications.delete()
                messages.success(request, f"Successfully deleted {count} applications.")
            
            # Bulk Status processing logic
            elif action in ["Approved", "Rejected", "Pending"]:
                for application in applications:
                    old_status = application.status
                    application.status = action
                    application.reviewed_at = timezone.now()
                    application.save()

                    AdminActivityLog.objects.create(
                        application=application,
                        admin=request.user,
                        action=f"Bulk status changed from {old_status} to {action}",
                    )
                messages.success(request, f"Successfully updated {len(application_ids)} applications to {action}.")

    return redirect("admin_applications")