import React, { useState } from "react";

export default function BookForm() {
  const [form, setForm] = useState({ title: "", author: "", price: "" });
  const [books, setBooks] = useState([]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch("http://localhost:8000/books/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...form, price: parseFloat(form.price) }),
    });
    setForm({ title: "", author: "", price: "" });
    loadBooks();
  };

  const loadBooks = async () => {
    const res = await fetch("http://localhost:8000/books/");
    const data = await res.json();
    setBooks(data);
  };

  React.useEffect(() => {
    loadBooks();
  }, []);

  return (
    <div className="p-4 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold mb-4">📚 Book Entry Form</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input name="title" placeholder="Title" value={form.title} onChange={handleChange} className="border p-2 rounded" required />
        <input name="author" placeholder="Author" value={form.author} onChange={handleChange} className="border p-2 rounded" required />
        <input name="price" placeholder="Price" type="number" step="0.01" value={form.price} onChange={handleChange} className="border p-2 rounded" required />
        <button type="submit" className="bg-blue-600 text-white p-2 rounded">Add Book</button>
      </form>

      <ul className="mt-6 border-t pt-4">
        {books.map((b) => (
          <li key={b.id} className="py-2">{b.title} — {b.author} (${b.price.toFixed(2)})</li>
        ))}
      </ul>
    </div>
  );
}
