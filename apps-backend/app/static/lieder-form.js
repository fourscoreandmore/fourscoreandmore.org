jQuery(document).ready(function( $ ) {
  // Hide the rest length field until preserveRestBars is checked.
  var restLengthField = $('input[name="restLength"]').parent('.form-field');
  if (restLengthField.length > 0) {
    $('input[name="preserveRestBars"]').change(function() {
      if ($(this).prop("checked") || restLengthField.find('.form-error').length) {
        restLengthField.show();
      } else {
        restLengthField.hide();
      }
    }).trigger('change');
  }

  // Hide the harmonic rhythm field until the chordHints feature is selected.
  var harmonicRhythmField = $('input[name="harmonicRhythm"]').parent('.form-field');
  if (harmonicRhythmField.length > 0) {
    $('select[name="addition"]').change(function() {
      if ($(this).val() === "chordHints" || harmonicRhythmField.find('.form-error').length) {
        harmonicRhythmField.show();
      } else {
        harmonicRhythmField.hide();
      }
    }).trigger('change');
  }
});
