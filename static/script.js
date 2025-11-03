document.getElementById("shortenBtn").addEventListener("click", async () => {
  const url = document.getElementById("urlInput").value.trim();
  if (!url) return alert("Please enter a URL!");

  const response = await fetch("/shorten/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ original_url: url }),
  });

  const data = await response.json();
  if (data.short_url) {
    document.getElementById("result").innerHTML =
      `Short URL: <a href="${data.short_url}" target="_blank">${data.short_url}</a>`;
  } else {
    document.getElementById("result").innerText = "Error creating short URL!";
  }
});
