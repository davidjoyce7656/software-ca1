from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            user_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Send email to the user
            send_mail(
                subject=f"Contact Form Submission from {name}",
                message=message,
                from_email=user_email,
                recipient_list=[user_email],  # Or change this to your email
            )
            
            # Optionally, send a thank you email to the user
            send_mail(
                subject="Thank you for contacting us!",
                message="We have received your message.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
            )
            
            # Redirect to the same contact page or another page after form submission
            return redirect('contact')  # This will redirect back to the contact form page (adjust URL if needed)
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})
