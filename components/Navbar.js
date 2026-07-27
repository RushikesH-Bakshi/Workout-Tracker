import Link from 'next/link';
import { useEffect, useState } from 'react';
import { getProfile, logout } from '../lib/api';
import { useRouter } from 'next/router';

export default function Navbar() {
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    let canceled = false;

    getProfile()
      .then((profile) => {
        if (!canceled) setUser(profile.user);
      })
      .catch(() => {
        if (!canceled) setUser(null);
      });

    return () => {
      canceled = true;
    };
  }, []);

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };

  return (
    <header className="navbar">
      <Link href="/">
        <a className="logo">Workout Logger</a>
      </Link>
      <div className="nav-links">
        <Link href="/api/getWorkouts">
          <a>All Workouts</a>
        </Link>
        <Link href="/api/profile">
          <a>Account</a>
        </Link>
        {user ? (
          <>
            <Link href="/api/newWorkout">
              <a className="button secondary">Add Workout</a>
            </Link>
            <button className="button" type="button" onClick={handleLogout}>
              Log Out
            </button>
          </>
        ) : (
          <>
            <Link href="/api/signin">
              <a className="button secondary">Sign In</a>
            </Link>
            <Link href="/api/login">
              <a className="button">Login</a>
            </Link>
          </>
        )}
      </div>
    </header>
  );
}
