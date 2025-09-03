// this Javascript is to improve interactivity on the 
// booking calendar page

$(document).ready(function() {
    //this will initializa the variables
    let selectedServices = [];
    let selectedDate = null;
    let selectedTime = null;
    let selectedEmployee = null;
    let serviceDetails = {};

    // this fucntion is to extract service details from the page
    $('.service-checkbox').each(function() {
            const serviceId = $(this).val();
            const price = parseFloat($(this).data('price'));
            const duration = parseInt($(this).data('duration'));
            const name = $(this).next('label').contents().first().text().trim().split(' - ')[0];

            serviceDetails[serviceId] = {
                name: name,
                price: price,
                duration: duration
            };

    });

    //this function is to enable service selection
    $('.service-checkbox').change(function() {
            selectedServices = [];
            $('.service-checkbox:checked').each(function() {
                selectedServices.push($(this).val());
            });
            updateServiceDetails();
            updateBookingSummary();
    });

    //selection for the date and employee
    $('#appointment-date, #employee-select').change(function() {
            selectedDate = $('#appointment-date').val();
            selectedEmployee = $('#employee-select').val();
            selectedTime = null; //this will reset the time when date or employee changes

            if (selectedDate && selectedEmployee) {
                loadAvailableSlots();
            } else {
                $('#available-slots').html('<small class="text-muted">Please select a date and stylist first</small>');
            }

            updateBookingSummary();

    });

    //this will help in time slot selection
    $(document).on('click', '.available-time-slot', function() {
            $('.available-time-slot').removeClass('selected btn-primary').addClass('btn-outline-primary');
            $(this).removeClass('btn-outline-primary').addClass('selected btn-primary');
            selectedTime = $(this).data('time');
            updateBookingSummary();
    });

    //this will help in updating service details like the price and duration
    function updateServiceDetails() {
            let totalPrice = 0;
            let totalDuration = 0;

            selectedServices.forEach(function(serviceId) {
               if (serviceDetails[serviceId]) {
                    totalPrice += serviceDetails[serviceId].price;
                    totalDuration += serviceDetails[serviceId].duration;
                }

            });

            $('#total-price').text(totalPrice.toFixed(2));
            $('#total-duration').text(totalDuration);

    }

    //this will load available time slots via AJAX
    function loadAvailableSlots() {
            showLoading(false);
            //will change false to true if i want the loading to be seen

            $.ajax({
                url: '/salon/get-available-slots/',
                type: 'GET',
                data: {
                    date: selectedDate,
                    employee_id: selectedEmployee,
                    services: selectedServices.join(',')
                },
                success: function(response) {
                    if (response.success) {
                        let slotsHtml = '';
                        if (response.available_slots && response.available_slots.length > 0) {
                            response.available_slots.forEach(function(slot) {

                                slotsHtml += `<button type="button" class="btn btn-outline-primary available-time-slot
                                mb-2 me-2" data-time="${slot}">${slot}</button>`;

                            });
                        } else {
                            slotsHtml += '<small class="text-muted">No available slots for this date</small>';
                        }
                        $('#available-slots').html(slotsHtml);

                    } else {
                        $('#available-slots').html('<small class="text-danger">Error loading available slots</small>');
                        console.error('Error:',response.message);
                    }  
                },
                error: function(xhr, status, error) {
                    $('#available-slots').html('<small class="text-danger">Error loading availabe slots</small>')
                    console.error('AJAX Error:', error);
                },
                complete: function() {
                    showLoading(false);
                }
            });

    }

    //this will update the booking summary
    function updateBookingSummary() {
            if (selectedServices.length > 0 && selectedDate && selectedTime && selectedEmployee) {
                let servicesList = '';
                let totalPrice = 0;
                let totalDuration = 0;

                selectedServices.forEach(function(serviceId) {
                    if (serviceDetails[serviceId]) {
                        servicesList += `<li>
                        ${serviceDetails[serviceId].name} - $${serviceDetails[serviceId].price.toFixed(2)}
                        </li>`;
                        totalPrice += serviceDetails[serviceId].price;
                        totalDuration += serviceDetails[serviceId].duration;
                    }
                });


                const summary = `
                    <h6>Selected Services:</h6>
                    <ul>${servicesList}</ul>
                    <p><strong>Date:</strong> ${formatDate(selectedDate)} </p>
                    <p><strong>Time:</strong> ${selectedTime} </p>
                    <p><strong>Stylist:</strong> ${$('#employee-select option:selected').text()} </p>
                    <p><strong>Total Price:</strong> ${totalPrice.toFixed(2)}</p>
                    <p><strong>Duration:</strong> ${totalDuration} minutes </p>
                `;

                $('#booking-summary').html(summary);
                $('#book-appointment-btn').prop('disabled', false);

            } else{
                let message = 'Please select';
                const missing = [];

                if (selectedServices.length === 0) missing.push('services');

                if(!selectedDate) missing.push('date');

                if(!selectedTime) missing.push('time');

                if(!selectedEmployee) missing.push('stylist');

                message += missing.join(', ') + ' to see the summary.';

                $('#booking-summary').html(`<p class="text-muted">${message}</p>`);
                // this will ensure that the summary updates along with the selected services section of the appointment
                $('#book-appointment-btn').prop('disabled', true);
            }
    }

    //this will enable the appointment booking handler
        $('#book-appointment-btn').click(function() {
            $('#modal-summary-content').html($('#booking-summary').html());
            $('#bookingModal').modal('show');
    });

    //this is to confirm the booking
    $('#confirm-booking').click(function() {
            showLoading(false);
            //will change false to true if i want the loading to be seen

            $.ajax({
                url: '/salon/book-appointment/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data: {
                    services: selectedServices,
                    scheduleDay: selectedDate,
                    appointmentTime: selectedTime,
                    employeeId: selectedEmployee
                },
                success: function(response) {
                    if (response.success) {
                        $('#bookingModal').modal('hide');
                        showSuccessMessage('Appointment booked successfully!');
                        //this will redirect to another page or clear the form after a successfull booking
                        
                        setTimeout(function() {
                            window.location.href = response.redirect_url || '/';
                        }, 2000);

                    } else {
                        alert('Error:' + response.message);
                    }
                },
                error: function(xhr, status, error) {

                    let errorMessage = "Error booking appointment. Please try again.";
                    if (xhr.responseJSON && xhr.responseJSON.message) {

                        errorMessage = xhr.responseJSON.message;
                    } else if (xhr.responseText) {

                        errorMessage = xhr.responseText;
                    }
                    alert('errorMessage');
                    console.error('Booking Error:', error, xhr.responseText);
                    // this code will inform me of any issue in the console and what is going wrong
                },
                complete: function() {
                    showLoading(false);
                }
            });
           
        });

    });

    //this is the utility function to get the CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');

            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();

                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    //this will format the date to be displayed
    function formatDate(dateString) {
        const options = {year: 'numeric', month: 'long', day: 'numeric'};
        return new Date(dateString).toLocaleDateString(undefined, options);
    }

    //this will show or hide the loading spinner
    function showLoading(show) {
        if (show) {
            $('#loading-spinner').removeClass('d-none');
        } else {
            $('#loading-spinner').addClass('d-none');
        }
    }
        
    //this will show success message after booking
    function showSuccessMessage(message) {
        const alert = $(`
            <div class="alert alert-success alert-dismissible fade show" role="alert"
            style="position: fixed; top:20px; right:20px; z-index:10000;">
                ${message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `);

        $('body').append(alert);
        setTimeout(function() {
            alert.alert('close');
        }, 3000);
    }    





        