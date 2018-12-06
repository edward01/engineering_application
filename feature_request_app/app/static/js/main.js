


// Modal Onshow Event
$('#entryModal').on('shown.bs.modal', function(e) {
    let $self = $(this);
    let $invoker = $(e.relatedTarget);
    // $self.find('input:not([type="hidden"])').first().focus();
});
