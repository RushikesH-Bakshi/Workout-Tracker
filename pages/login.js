import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { login } from '../lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({ email: '', password: '', remember: false });
  const [error, setError] = useState('');

  useEffect(() => {
    const handleSubmit = async (event) => {
      event.preventDefault();
      try {
        await login(form);
        router.push('/');
      } catch (err) {
        setError(err.message);
      }
    };
  
    return (
      <section className="card">
        <h1 className="page-title">Login</h1>
        {error ? <div className="alert">{error}</div> : null}
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              required
              value={form.email}
              onChange={(event) => setForm({ ...form, email: event.target.value })}
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              required
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
            />
          </div>
          <div className="input-group">
            <label>
              <input
                type="checkbox"
                checked={form.remember}
                onChange={(event) => setForm({ ...form, remember: event.target.checked })}
              />{' '}
              Remember me
            </label>
          </div>
          <input className="button" type="submit" value="Login" />
        </form>
      </section>
    );
    
  })
}
