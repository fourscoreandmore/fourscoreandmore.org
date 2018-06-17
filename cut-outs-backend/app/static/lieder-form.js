jQuery(document).ready(function( $ ) {
  // Hide the rest length field until preserveRestBars is checked.
  var restLengthField = $('input[name="restLength"]').parent('.form-field');
  if (restLengthField.length > 0) {
    restLengthField.hide();
    $('input[name="preserveRestBars"]').change(function() {
      if ($(this).prop('checked')) {
        restLengthField.show();
      } else {
        restLengthField.hide();
      }
    });
  }

  // Hide the harmonic rhythm field until the chordHints feature is selected.
  var harmonicRhythmField = $('input[name="harmonicRhythm"]').parent('.form-field');
  if (harmonicRhythmField.length > 0) {
    harmonicRhythmField.hide();
    $('select[name="addition"]').change(function() {
      if ($(this).val() === "chordHints") {
        harmonicRhythmField.show();
      } else {
        harmonicRhythmField.hide();
      }
    });
  }
});
