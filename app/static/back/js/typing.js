        // JavaScript to dynamically set the text and width
        const paragraph = "Can you find the sentence that shows the perfect feeling? ";

        // Select the element
        const dynamicTextElement = document.getElementById("dynamic-text");

        // Set the text content
        dynamicTextElement.textContent = paragraph;

        // Calculate and set the width based on the content length
        dynamicTextElement.style.width = `${paragraph.length}ch`;