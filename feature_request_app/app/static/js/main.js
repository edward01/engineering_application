let startDate = moment().format('L');

// Class to represent a row
function FeatureRequestRow(data) {
    var self = this;
    self.id = data.id;
    self.priority = ko.observable();
    self.title = ko.observable();
    self.description = ko.observable();
    self.target_date = ko.observable();
    self.client = ko.observable();
    self.product_area = ko.observable();
    self.is_highlighed = ko.observable(false);

    self.update = function(data) {
        self.priority(data.priority);
        self.title(data.title);
        self.description(data.description);
        self.target_date(data.target_date);
        self.client(data.client);
        self.product_area(data.product_area);
    }
    self.update(data);
}


// Overall viewmodel for this screen, along with initial state
function FeatureRequestsViewModel() {
    var self = this;
    //----------------
    // Selections
    //----------------
    self.available_clients = app_vars.data_choices.clients;
    self.available_product_areas = app_vars.data_choices.product_areas;

    //----------------
    // Main entries fields
    //----------------
    self.active_entries = ko.observableArray([]);
    self.completed_entries = ko.observableArray([]);
    self.chosen_client = ko.observable();
    self.showLoader = ko.observable(true);
    self.showCompletedItems = ko.observable(false);
    self.highlighted_priority = 0;

    //----------------
    // Modal fields
    //----------------
    self.modal_title = ko.observable();
    self.selected_item = ko.observable();
    self.selected_item_editable = ko.observable();

    //----------------
    // Computed data
    //----------------
    self.modal_title = ko.computed(function() {
        if (self.selected_item_editable())
            return self.selected_item_editable().id == 0? 'New': 'Edit';
        return '';
    });
    self.chosen_client_text = ko.computed(function() {
        let elementPos = self.available_clients.map(function(x) {return x.value; }).indexOf(self.chosen_client());
        if (elementPos >= 0)
            return self.available_clients[elementPos].text;
        return '';
    });

    //----------------
    // Utilities
    //----------------
    function loadDefaultClient() {
        let defaultClient = location.hash.replace('#', '');
        if (defaultClient == '')
            self.goToClient(self.available_clients[0]);
        else {
            let elementPos = self.available_clients.map(function(x) {return x.value; }).indexOf(defaultClient);
            if (elementPos >= 0)
                self.goToClient(self.available_clients[elementPos]);
        }
    }
    function ajaxGet(callback) {
        $.getJSON(app_vars.url.records.replace('client_arg', self.chosen_client()), function(data) {
            let active_entries = [];
            let completed_entries = [];
            $.each(data, function (ctr, item) {
                if (item.priority > 0) active_entries.push(new FeatureRequestRow(item));
                else completed_entries.push(new FeatureRequestRow(item));
            });
            self.active_entries(active_entries);
            self.completed_entries(completed_entries);
            self.showLoader(false);
            $('.invisible').removeClass('invisible');
            if ($('.navbar-collapse').hasClass('show')) $('.navbar-toggler').click();
            if (typeof callback !== 'undefined') callback();
        });
    }
    function ajaxPost(options) {
        // url, params, success_callback, success_message
        $.post(options.url, options.params, function (response) {
            if (response.success) {
                options.success_callback(response);
                notie.alert({type: 'success', text: '<i class="fa fa-check" aria-hidden="true"></i> '+ options.success_message});
            }
            else {
                let errors = 'Check for the following errors:';
                $.each(response.errors, function(i, item) {
                    errors += '<br>* '+ i +': '+ item;
                });
                notie.alert({type: 'error', text: '<i class="fa fa-exclamation-circle" aria-hidden="true"></i> '+ errors, stay: true});
            }
        }).fail(function () {
            notie.alert({
                type: 'error',
                text: `<i class="fa fa-exclamation-circle" aria-hidden="true"></i>
                        Processing failed, please try again later
                        <a class="btn btn-secondary" href="/" role="button">
                            <i class="fas fa-sync-alt"></i> Refresh
                        </a>`,
                stay: true
            });
        }).always(function() {

        });
    }
    function initDatePicker() {
        let pickerStartDate = (self.selected_item_editable().target_date() < startDate)?
                self.selected_item_editable().target_date():
                startDate;
        $('[data-toggle="datepicker"]').datepicker({
            autoHide: true,
            autoPick: true,
            date: self.selected_item_editable().target_date(),
            startDate: pickerStartDate,
            zIndex: 2048
        });
    }

    //----------------
    // Events
    //----------------
    self.modalSubmit = function() {
        if (typeof self.selected_item_editable().priority() == 'undefined' || self.selected_item_editable().priority() == '')
            self.selected_item_editable().priority(self.active_entries().length + 1);
        self.highlighted_priority = self.selected_item_editable().priority();
        ajaxPost({
            url: app_vars.url.upsert,
            params: $('#formSubmit').serialize(),
            success_callback: function(response) {
                let selected_item = self.selected_item(),
                    updatedItem = ko.toJS(self.selected_item_editable());
                if (response.update_priority) {
                    // refresh listing / insert mode
                    ajaxGet();
                }
                else {
                    // edit mode
                    selected_item.update(updatedItem);
                }
            },
            success_message: 'Saving Successful'
        });
    }
    self.setEmptyModal = function() {
        self.selected_item_editable(new FeatureRequestRow({
            id: 0,
            client: self.chosen_client(),
            target_date: startDate
        }));
        initDatePicker();
    }
    self.loadSelectedItem = function(item) {
        self.selected_item(item);
        self.selected_item_editable(new FeatureRequestRow(ko.toJS(item)));
        initDatePicker();
    }
    self.removeRow = function(item) {
        notie.confirm({ text: 'Are you sure to delete this record? <br>"'+ item.title() +'"' }, function() {
            ajaxPost({
                url: app_vars.url.delete.replace('0', item.id),
                params: {csrf_token: app_vars.ct},
                success_callback: function() {
                    ajaxGet();
                },
                success_message: 'Selected record has been deleted'
            });
        });
    }
    self.completeRow = function(item) {
        notie.confirm({ text: 'Mark this record as complete? <br>"'+ item.title() +'"' }, function() {
            ajaxPost({
                url: app_vars.url.complete.replace('0', item.id),
                params: {csrf_token: app_vars.ct},
                success_callback: function() {
                    ajaxGet();
                },
                success_message: 'Selected record has been completed'
            });
        });
    }
    self.dragNewPriority = function(current_priority, new_priority, $dragger_div) {
        self.highlighted_priority = new_priority;
        ajaxPost({
            url: app_vars.url.update_priority,
            params: {
                csrf_token: app_vars.ct,
                client: self.chosen_client(),
                current_priority: current_priority,
                new_priority: new_priority
            },
            success_callback: function() {
                $dragger_div.remove();
                ajaxGet(function() { fr_model.set_highlighted_priority(); });
            },
            success_message: 'Priority has been updated'
        });
    }
    self.set_highlighted_priority = function() {
        if (self.highlighted_priority == 0) return;
        $([document.documentElement, document.body]).animate({
            scrollTop: $("#heading"+ self.active_entries()[self.highlighted_priority-1].id).offset().top - 200
        }, 1000);
        self.active_entries()[self.highlighted_priority-1].is_highlighed(true);
        setTimeout(() => {
            self.active_entries()[self.highlighted_priority-1].is_highlighed(false);
            self.highlighted_priority = 0;
        }, 3000);
    }
    self.goToClient = function(item) {
        self.showLoader(true);
        location.hash = item.value;
        self.chosen_client(item.value);
        ajaxGet();
    }

    //----------------
    // Onload Event
    //----------------
    loadDefaultClient();
}
var fr_model = new FeatureRequestsViewModel();
ko.applyBindings(fr_model);


//---------------- [BACK TO TOP] ---------------------
$(window).scroll(function () {
    if ($(this).scrollTop() > 50) {
        $('#back-to-top').fadeIn();
    } else {
        $('#back-to-top').fadeOut();
    }
});
$('#back-to-top').click(function () {
    $('#back-to-top').tooltip('hide');
    $('body,html').animate({
        scrollTop: 0
    }, 500);
    return false;
});


//---------------- [BOOTSTRAP MODAL] ---------------------
$('#entryModal').on('hidden.bs.modal', function(e) {
    fr_model.set_highlighted_priority();
});


//---------------- [JQUERY DRAGGABLE] ---------------------
var sortable_items = document.getElementById('accordionItems');
Sortable.create(sortable_items, {
    handle: ".my-handle",
    onEnd: function (evt) {
        fr_model.dragNewPriority(evt.oldIndex+1, evt.newIndex+1, $(evt.item));
    },
});


$(function() {
    $('[data-toggle="tooltip"]').tooltip();
});
