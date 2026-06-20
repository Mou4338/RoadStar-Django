import { useState } from "react";

export default function Register() {
  const [form, setForm] = useState({
    username: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch("/djangoapp/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: form.username,
          first_name: form.firstName,
          last_name: form.lastName,
          email: form.email,
          password: form.password,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Registration failed");
        return;
      }
      setSuccess(true);
      window.location.href = "/";
    } catch (err) {
      setError("Something went wrong. Please try again.");
    }
  };

  return (
    <section className="form-shell">
      <div>
        <span className="eyebrow">JOIN ROADSTAR</span>
        <h1>Create your account</h1>
        <p>Five fields. One minute. A better car-buying experience.</p>
      </div>

      {error && <p className="error">{error}</p>}
      {success && <p className="success">Account created — redirecting…</p>}

      <form className="panel" onSubmit={handleSubmit}>
        <div className="twocol">
          <label>
            First name
            <input name="firstName" value={form.firstName} onChange={update("firstName")} required />
          </label>
          <label>
            Last name
            <input name="lastName" value={form.lastName} onChange={update("lastName")} required />
          </label>
        </div>
        <label>
          Username
          <input name="username" value={form.username} onChange={update("username")} required />
        </label>
        <label>
          Email
          <input name="email" type="email" value={form.email} onChange={update("email")} required />
        </label>
        <label>
          Password
          <input name="password" type="password" value={form.password} onChange={update("password")} required />
        </label>
        <button type="submit">Register</button>
      </form>
    </section>
  );
}
