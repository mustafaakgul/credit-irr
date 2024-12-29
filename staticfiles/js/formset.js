
function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+-)');
    var replacement = prefix + '-' + ndx + '-';
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
    replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm(btn, prefix) {
    alert("addForm");
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (formCount < 1000) {
        // Clone a formset1 (without event handlers) from the first formset1
        var row = $(".item:last").clone(false).get(0);

        // Insert it after the last formset1
        $(row).removeAttr('id').hide().insertAfter(".item:last").slideDown(300);

        // Remove the bits we don't want in the new row/formset1
        // e.g. error messages
        $(".errorlist", row).remove();
        $(row).children().removeClass("error");

        // Relabel or rename all the relevant bits
        $(row).find('.formset-field').each(function () {
            updateElementIndex(this, prefix, formCount);
            $(this).val('');
            $(this).removeAttr('value');
            $(this).prop('checked', false);
        });

        // Add an event handler for the delete item/formset1 link
        $(row).find(".delete").click(function () {
            return deleteForm(this, prefix);
        });
        // Update the total formset1 count
        $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);

    } // End if

    return false;
}


function deleteForm(btn, prefix) {
      var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
      if (formCount > 1) {
          // Delete the item/formset1
          var goto_id = $(btn).find('input').val();
          if( goto_id ){
            $.ajax({
                url: "/" + window.location.pathname.split("/")[1] + "/formset-data-delete/"+ goto_id +"/?next="+ window.location.pathname,
                error: function () {
                  console.log("error");
                },
                success: function (data) {
                  $(btn).parents('.item').remove();
                },
                type: 'GET'
            });
          }else{
            $(btn).parents('.item').remove();
          }

          var forms = $('.item'); // Get all the forms
          // Update the total number of forms (1 less than before)
          $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
          var i = 0;
          // Go through the forms and set their indices, names and IDs
          for (formCount = forms.length; i < formCount; i++) {
              $(forms.get(i)).find('.formset-field').each(function () {
                  updateElementIndex(this, prefix, i);
              });
          }
      } // End if

      return false;
  }

  $("body").on('click', '.remove-formset1-row',function () {
    deleteForm($(this), String($('.add-formset1-row').attr('id')));
  });

  $("body").on('click', '.add-formset1-row',function () {
      return addForm($(this), String($(this).attr('id')));
  });