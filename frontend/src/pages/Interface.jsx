import { Chat } from '../components/Chat';
import { NavbarDefault } from '../components/Navbar';

export function Interface() {
  
  return (
    <div>
      <div>
        <NavbarDefault />
        <main>
          <Chat />
        </main>
      </div>
    </div>
  );
}
