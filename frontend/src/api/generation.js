const api_link = "http://127.0.0.1:8000";
const endpoints = {
    content: `${api_link}/api/generate-content`,
    bio: `${api_link}/api/generate-bio`
};

async function generateProductContent(data) {
    try {
        const response = await fetch(endpoints.content, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
        });

        if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();
        console.log("Generated Product Content:", result);
        return result;
    } catch (error) {
        console.error("Error generating product content:", error);
        return null;
    }
};

async function generateArtisanBio(data) {
    try {
        const response = await fetch(endpoints.bio, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
        });

        if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();
        console.log("Generated Artisan Bio:", result);
        return result;
    } catch (error) {
        console.error("Error generating artisan bio:", error);
        return null;
    }
};

export {generateArtisanBio, generateProductContent};