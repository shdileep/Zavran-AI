// Supabase Client Initialization (Browser & Node.js)
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://yhgfdzwelegsmxixmuun.supabase.co';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY || process.env.SUPABASE_ANON_KEY || 'sb_publishable_BcyUOzXvvkaYCqV0GrvbNA_V0RToaF8';

export const supabase = createClient(supabaseUrl, supabaseKey);
