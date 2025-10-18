// this Javascript is to improve interactivity on the
// booking calendar page

$(document).ready(function() {
    //this will initialize the variables
    let selectedServices = [];
    let selectedDate = null;
    let selectedTime = null;
    let selectedEmployee = null;
    let serviceDetails = {};

    // Initialize service details from the template data
    initializeServiceDetails();

    function initializeServiceDetails() {
        // This function will be populated when services are loaded via AJAX
        serviceDetails = {};

        // Populate serviceDetails from the template data
        $('.service-checkbox').each(function() {
            const $this = $(this);
            const id = $this.val();
            serviceDetails[id] = {
                name: $this.data('name'),
                price: parseFloat($this.data('price')),
                duration: $this.data('duration')
            };
        });
    }

    //this function is to enable service selection
    $('.service-checkbox').change(function() {
            selectedServices = [];
            $('.service-checkbox:checked').each(function() {
                selectedServices.push($(this).val());
            });

            updateServiceDetails();
            updateBookingSummary();
            updateTotalDuration();
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
                    totalDuration += parseDuration(serviceDetails[serviceId].duration);
                }

            });

            $('#total-price').text(totalPrice.toFixed(2));
            $('#total-duration').text(formatDuration(minutesToHHMMSS(totalDuration)));

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
                        ${serviceDetails[serviceId].name} - ${serviceDetails[serviceId].price.toFixed(2)}
                        </li>`;
                        totalPrice += serviceDetails[serviceId].price;
                        totalDuration += parseDuration(serviceDetails[serviceId].duration);
                    }
                });


                const summary = `
                    <h6>Selected Services:</h6>
                    <ul>${servicesList}</ul>
                    <p><strong>Date:</strong> ${formatDate(selectedDate)} </p>
                    <p><strong>Time:</strong> ${selectedTime} </p>
                    <p><strong>Stylist:</strong> ${$('#employee-select option:selected').text()} </p>
                    <p><strong>Total Price:</strong> ${totalPrice.toFixed(2)}</p>
                    <p><strong>Duration:</strong> ${formatDuration(minutesToHHMMSS(totalDuration))}</p>
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
        $('#book-appointment-btn').click(function(e) {
            e.preventDefault();
            showLoading(false);
            //will change false to true if i want the loading to be seen

            // Validate data before sending
            if (!validateBookingData()) {
                return;
            }

            console.log('Sending data:', {
                services: selectedServices,
                scheduleDay: selectedDate,
                appointmentTime: selectedTime,
                employeeId: selectedEmployee
            });

            $.ajax({
                url: '/salon/book-appointment/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data: {
                    services: selectedServices.join(','),
                    scheduleDay: selectedDate,
                    appointmentTime: selectedTime,
                    employeeId: selectedEmployee
                },
                success: function(response) {
                    if (response.success) {
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
                    if (xhr.responseJSON) {
                        if (xhr.responseJSON.message) {
                            errorMessage = xhr.responseJSON.message;
                        }
                        if (xhr.responseJSON.errors) {
                            let errorDetails = '';
                            for (let field in xhr.responseJSON.errors) {
                                errorDetails += field + ': ' + xhr.responseJSON.errors[field].join(', ') + '\n';
                            }
                            errorMessage += '\n' + errorDetails;
                        }
                    } else if (xhr.responseText) {
                        errorMessage = xhr.responseText;
                    }
                    alert(errorMessage);
                    console.error('Booking Error:', error, xhr.responseText);
                    // this code will inform me of any issue in the console and what is going wrong
                },
                complete: function() {
                    showLoading(false);
                }
            });

        });

    // Function to validate booking data before sending
    function validateBookingData() {
        let errors = [];

        if (selectedServices.length === 0) {
            errors.push('Please select at least one service.');
        }

        if (!selectedDate) {
            errors.push('Please select a date.');
        } else {
            const selectedDateObj = new Date(selectedDate);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            if (selectedDateObj < today) {
                errors.push('Please select a date that is not in the past.');
            }
        }

        if (!selectedTime) {
            errors.push('Please select a time slot.');
        }

        if (!selectedEmployee) {
            errors.push('Please select a stylist.');
        }

        if (errors.length > 0) {
            alert('Please correct the following errors:\n' + errors.join('\n'));
            return false;
        }

        return true;
    }

    function parseDuration(durationStr) {
        const parts = durationStr.split(':');
        const hours = parseInt(parts[0], 10) || 0;
        const minutes = parseInt(parts[1], 10) || 0;
        return hours * 60 + minutes;

    }

    //this function will change the format in which the time is being displayed from HH:MM:SS to something like 1 hour 45 mins
    function formatDuration(durationStr) {
        //this will use the data that is  hh:mm:ss format like it is in the database and convert it to human readable time like 1 hour and 45 minutes
        const parts = durationStr.split(':');
        const hours = parseInt(parts[0], 10) || 0;
        const minutes = parseInt(parts[1], 10) || 0;
        let result = '';
        if (hours > 0) result += `${hours} hour${hours > 1 ? 's' : ''}`;
        //this means that when a hour number is more than 0 add the label of hour and if it is more than 1 hour add an (s)
        if (hours > 0  && minutes > 0) result += ' ';
        if (minutes > 0) result += `${minutes} minute${minutes > 1 ? 's' : ''}`;
        if (result === '') result = '0 minutes';
        return result
    }

    function updateTotalDuration() {
        let totalMinutes = 0;
        $('.service-checkbox:checked').each(function() {
            const duration = $(this).data('duration');
            totalMinutes += parseDuration(duration);
        });//this will sum the duration by converting time from hh:mm:ss to minutes

        //this converts  the time from minutes back to HH:MM:SS
        const hhmmss = minutesToHHMMSS(totalMinutes);
        $('#total-duration').text(formatDuration(hhmmss));
    }

    // since I am changing the time format to be like {1 hour 45 minutes} in order to calculate the total service
    //time i will need to convert the time back to HH:MM:SS format for calculation and then will be converted back to human readable format after the calculation is complete
    function minutesToHHMMSS(totalMinutes) {
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;
        return`${hours}:${minutes < 10 ? '0' : ''}${minutes}:00`;
    }

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
