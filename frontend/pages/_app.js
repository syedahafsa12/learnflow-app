import '../styles/globals.css';
import { UserProvider } from '../context/UserContext';
import Layout from '../components/Layout';

function MyApp({ Component, pageProps }) {
  return (
    <UserProvider>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </UserProvider>
  );
}

export default MyApp;