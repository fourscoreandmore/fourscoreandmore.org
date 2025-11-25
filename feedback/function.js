function generateFeedback() {
  // Process each topic to get the feedback with text comments
  let combinedPositives = '';
  let combinedNegatives = '';

  // Get all topics (each has a text input with matching id)
  const topics = document.querySelectorAll('#options_from_file input[type="text"]');

  topics.forEach(topicInput => {
    const topicName = topicInput.id;
    const radioButtons = document.querySelectorAll(`input[type="radio"][name="${topicName}"]`);
    let selectedRadio = null;

    // Find the selected radio button for this topic
    for (let i = 0; i < radioButtons.length; i++) {
      if (radioButtons[i].checked) {
        selectedRadio = radioButtons[i];
        break;
      }
    }

    // Only process if a non-N/A option is selected
    if (selectedRadio && selectedRadio.getAttribute('data-tag') !== 'Neutral') {
      const text = topicInput.value.trim();
      const value = selectedRadio.value;

      // Append value + text (if text exists) to the appropriate feedback section
      if (selectedRadio.getAttribute('data-tag') === 'Positive') {
        combinedPositives += value + (text ? ' ' + text : '') + ' ';
      } else if (selectedRadio.getAttribute('data-tag') === 'Negative') {
        combinedNegatives += value + (text ? ' ' + text : '') + ' ';
      }
    }
  });

  // Update the feedback sections
  document.getElementById('positives').innerHTML = combinedPositives;
  document.getElementById('negatives').innerHTML = combinedNegatives;

  // Overall feedback (unchanged)
  let overallCombined = 'This essay on ';
  const userInputSubject = document.getElementById("userInputSubject").value.trim();
  const userInputAdjective = document.getElementById("userInputAdjective").value.trim();
  const userInputExplanation = document.getElementById("userInputExplanation").value.trim();

  if (userInputSubject) {
    overallCombined += userInputSubject;
  }

  overallCombined += ' is '

  if (userInputAdjective) {
    overallCombined += userInputAdjective;
  }

  overallCombined += '. '

  if (userInputExplanation) {
    overallCombined += userInputExplanation;
  }

  document.getElementById('overall').innerHTML = overallCombined;
}

// Collapsible functionality (unchanged)
document.querySelectorAll('.collapsible-header').forEach(header => {
  header.addEventListener('click', function() {
    const content = this.nextElementSibling;
    const icon = this.querySelector('.toggle-icon');

    content.classList.toggle('show');
    icon.textContent = content.classList.contains('show') ? '-' : '+';
  });
});