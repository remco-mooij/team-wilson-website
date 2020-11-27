function CollapseNewHire(attr1, attr2) {
    $(document).ready(function() {
        $(attr1).on('mouseenter', function() {
            $(attr2).fadeIn(400);
        });
        $(attr1).on('mouseleave', function() {
            $(attr2).fadeOut(400);
        });                    
    });
}