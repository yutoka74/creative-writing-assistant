$(document).ready(function() {
    let sentimentChart = null;
    let emotionChart = null;
    
    // Handle the analyze button click
    $('#analyzeBtn').click(function() {
        const text = $('#textInput').val().trim();
        
        if (text === '') {
            alert('Please enter some text to analyze.');
            return;
        }
        
        // Store a reference to the button
        const $analyzeBtn = $(this);
        
        // Change button state during analysis
        $analyzeBtn.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...');
        $analyzeBtn.prop('disabled', true);
        
        // Send analysis request
        $.ajax({
            url: '/analyze',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ text: text }),
            success: function(response) {
                // Display analysis results
                displayResults(response);
                
                // Reset button to original state - directly within the callback
                $analyzeBtn.html('Analyze Emotional Tone');
                $analyzeBtn.prop('disabled', false);
            },
            error: function(error) {
                console.error('Error:', error);
                alert('An error occurred during analysis. Please try again.');
                
                // Reset button in case of error as well
                $analyzeBtn.html('Analyze Emotional Tone');
                $analyzeBtn.prop('disabled', false);
            },
            // Add a timeout setting
            timeout: 30000  // 30 seconds
        });
    });
    
    // Handle the suggest button click
    $('#suggestBtn').click(function() {
        const text = $('#textInput').val().trim();
        const targetEmotion = $('#targetEmotion').val();
        
        if (text === '') {
            alert('Please enter some text first.');
            return;
        }
        
        // Show loading state
        $(this).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...');
        $(this).prop('disabled', true);
        
        // Get suggestions
        $.ajax({
            url: '/suggestions',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 
                text: text,
                target_emotion: targetEmotion
            }),
            success: function(response) {
                displaySuggestions(response);
                // Reset button text and enable it again
                setTimeout(function() {
                    $('#suggestBtn').html('Get Suggestions');
                    $('#suggestBtn').prop('disabled', false);
                }, 100);
            },
            error: function(error) {
                console.error('Error:', error);
                alert('An error occurred while generating suggestions. Please try again.');
                $('#suggestBtn').html('Get Suggestions');
                $('#suggestBtn').prop('disabled', false);
            }
        });
    });
    
    // Function to display analysis results
    function displayResults(data) {
        // Show results container
        $('#results').removeClass('d-none');
        
        // Display overall sentiment
        const sentimentText = data.document_sentiment.overall_sentiment.charAt(0).toUpperCase() + 
                             data.document_sentiment.overall_sentiment.slice(1);
        $('#overallSentiment').text(sentimentText);
        
        // Display dominant emotion
        const emotionText = data.document_emotions.dominant_emotion.charAt(0).toUpperCase() + 
                           data.document_emotions.dominant_emotion.slice(1);
        $('#dominantEmotion').text(emotionText);

        // Display emotional arc image
        $('#emotionalArc').attr('src', 'data:image/png;base64,' + data.plot_url);
        
        // Display emotion radar chart
        $('#emotionRadar').attr('src', 'data:image/png;base64,' + data.radar_plot_url);
        
        // Create sentiment chart
        if (sentimentChart) {
            sentimentChart.destroy();
        }
        
        const sentimentCtx = document.getElementById('sentimentChart').getContext('2d');
        
        const sentimentLabels = [];
        const sentimentData = [];
        const sentimentColors = [];
        
        for (const [label, score] of Object.entries(data.document_sentiment.scores)) {
            sentimentLabels.push(label.toLowerCase());
            sentimentData.push(score);
            
            if (label.toLowerCase() === 'positive') {
                sentimentColors.push('rgba(40, 167, 69, 0.6)'); // green
            } else {
                sentimentColors.push('rgba(220, 53, 69, 0.6)'); // red
            }
        }
        
        sentimentChart = new Chart(sentimentCtx, {
            type: 'bar',
            data: {
                labels: sentimentLabels,
                datasets: [{
                    label: 'Sentiment Score',
                    data: sentimentData,
                    backgroundColor: sentimentColors,
                    borderColor: sentimentColors.map(color => color.replace('0.6', '1')),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            callback: function(value) {
                                return (value * 100) + '%';
                            }
                        }
                    }
                }
            }
        });
        
        // Create emotion chart
        if (emotionChart) {
            emotionChart.destroy();
        }
        
        const emotionCtx = document.getElementById('emotionChart').getContext('2d');
        
        // Set colors for emotions
        const emotionColors = {
            joy: 'rgba(40, 167, 69, 0.6)',
            sadness: 'rgba(23, 162, 184, 0.6)',
            anger: 'rgba(220, 53, 69, 0.6)',
            fear: 'rgba(111, 66, 193, 0.6)',
            surprise: 'rgba(255, 193, 7, 0.6)',
            disgust: 'rgba(73, 80, 87, 0.6)',
            neutral: 'rgba(108, 117, 125, 0.6)'
        };
        
        const emotionBorderColors = {
            joy: 'rgba(40, 167, 69, 1)',
            sadness: 'rgba(23, 162, 184, 1)',
            anger: 'rgba(220, 53, 69, 1)',
            fear: 'rgba(111, 66, 193, 1)',
            surprise: 'rgba(255, 193, 7, 1)',
            disgust: 'rgba(73, 80, 87, 1)',
            neutral: 'rgba(108, 117, 125, 1)'
        };
        
        const emotions = data.document_emotions.scores;
        const emotionLabels = [];
        const emotionData = [];
        const colors = [];
        const borderColors = [];
        
        for (const [emotion, score] of Object.entries(emotions)) {
            emotionLabels.push(emotion);
            emotionData.push(score);
            colors.push(emotionColors[emotion] || 'rgba(108, 117, 125, 0.6)');
            borderColors.push(emotionBorderColors[emotion] || 'rgba(108, 117, 125, 1)');
        }
        
        emotionChart = new Chart(emotionCtx, {
            type: 'bar',
            data: {
                labels: emotionLabels,
                datasets: [{
                    label: 'Emotion Score',
                    data: emotionData,
                    backgroundColor: colors,
                    borderColor: borderColors,
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            callback: function(value) {
                                return (value * 100) + '%';
                            }
                        }
                    }
                }
            }
        });
        
        // Display consistency information
        if (!data.consistency_check.is_consistent) {
            $('#consistencyCard').removeClass('d-none');
            
            let consistencyHtml = `<p>Main emotion throughout the text is <strong>${data.consistency_check.main_emotion}</strong>, but some paragraphs have different emotions:</p><ul>`;
            
            data.consistency_check.inconsistencies.forEach(function(item) {
                consistencyHtml += `<li>Paragraph ${item.paragraph_index + 1} shows <span class="emotion-tag emotion-${item.emotion}">${item.emotion}</span> instead of <span class="emotion-tag emotion-${item.main_emotion}">${item.main_emotion}</span></li>`;
            });
            
            consistencyHtml += '</ul>';
            $('#consistencyBody').html(consistencyHtml);
        } else {
            $('#consistencyCard').addClass('d-none');
        }
        
        // Display emotional shifts
        if (data.emotional_shifts && data.emotional_shifts.length > 0) {
            $('#shiftsCard').removeClass('d-none');
            
            let shiftsHtml = '<p>Significant emotional shifts detected:</p>';
            
            data.emotional_shifts.forEach(function(shift) {
                shiftsHtml += `
                <div class="shift-item mb-3">
                    <p>Shift from <span class="emotion-tag emotion-${shift.from_emotion}">${shift.from_emotion}</span> to 
                    <span class="emotion-tag emotion-${shift.to_emotion}">${shift.to_emotion}</span>:</p>
                    <div class="sentence-highlight">"${shift.from_sentence}"</div>
                    <div class="sentence-highlight">"${shift.to_sentence}"</div>
                </div>`;
            });
            
            $('#shiftsBody').html(shiftsHtml);
        } else {
            $('#shiftsCard').addClass('d-none');
        }
    }
    
    // Function to display suggestions
    function displaySuggestions(data) {
        $('#suggestions').removeClass('d-none');
        
        let suggestionsHtml = `<p>Current dominant emotion: <span class="emotion-tag emotion-${data.current_dominant_emotion}">${data.current_dominant_emotion}</span></p>
                              <p>Target emotion: <span class="emotion-tag emotion-${data.target_emotion}">${data.target_emotion}</span></p>`;
        
        // Display specific sentence replacement suggestions if available
        if (data.specific_suggestions && data.specific_suggestions.length > 0) {
            suggestionsHtml += `<h5 class="mt-4">Specific Sentence Improvements:</h5>`;
            
            data.specific_suggestions.forEach(function(suggestion, index) {
                suggestionsHtml += `
                <div class="card mb-3">
                    <div class="card-header bg-light">
                        <small>Current emotion: <span class="emotion-tag emotion-${suggestion.emotion.current}">${suggestion.emotion.current}</span> → 
                        Target: <span class="emotion-tag emotion-${suggestion.emotion.target}">${suggestion.emotion.target}</span></small>
                    </div>
                    <div class="card-body p-3">
                        <div class="original-text mb-2">
                            <h6>Original:</h6>
                            <p class="pl-2 py-1 border-left border-danger">${suggestion.original}</p>
                        </div>
                        <div class="improved-text">
                            <h6>Improved:</h6>
                            <p class="pl-2 py-1 border-left border-success">${suggestion.improved}</p>
                        </div>
                    </div>
                </div>`;
            });
        }
        
        // Display general suggestions
        if (data.general_suggestions && data.general_suggestions.length > 0) {
            suggestionsHtml += `<h5 class="mt-4">General Improvement Strategies:</h5>`;
            
            data.general_suggestions.forEach(function(suggestion) {
                suggestionsHtml += `<div class="suggestion-item">${suggestion}</div>`;
            });
        }
        
        $('#suggestions').html(suggestionsHtml);
    }
    
    // Initialize with some sample text (optional)
    $('#textInput').val(`The morning dawned bright and beautiful. Birds sang in the trees and a gentle breeze carried the scent of flowers through the open window.

But as the day wore on, dark clouds gathered on the horizon. The wind picked up, scattering leaves across the yard. The birds fell silent.

By evening, a storm raged outside. Lightning flashed and thunder crashed, shaking the windows. The power went out, leaving the house in darkness.

When morning came again, the storm had passed. Sunlight glinted off raindrops clinging to leaves. A rainbow arched across the sky, promising better days ahead.`);
});
