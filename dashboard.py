"""
Mason's Famous Lobsters P&L Dashboard
Built with Panel
"""

import panel as pn
import pandas as pd
import hvplot.pandas
from datetime import datetime
from database import FinancialDatabase
from auth import SimpleAuth
from config import DASHBOARD_TITLE, DASHBOARD_PORT, LOCATIONS

# Enable Panel extensions
pn.extension('tabulator', sizing_mode="stretch_width")

# Initialize
db = FinancialDatabase()
auth = SimpleAuth()


class PLDashboard:
    """P&L Dashboard for Mason's Famous Lobsters"""

    def __init__(self):
        self.authenticated = False
        self.current_user = None
        self.setup_login()
        self.setup_dashboard()

    def setup_login(self):
        """Setup login interface"""
        self.username_input = pn.widgets.TextInput(
            name='Username',
            placeholder='Enter username'
        )
        self.password_input = pn.widgets.PasswordInput(
            name='Password',
            placeholder='Enter password'
        )
        self.login_button = pn.widgets.Button(
            name='Login',
            button_type='primary'
        )
        self.login_message = pn.pane.Markdown("")

        self.login_button.on_click(self.handle_login)

        self.login_panel = pn.Column(
            pn.pane.Markdown(f"# {DASHBOARD_TITLE}"),
            pn.pane.Markdown("## Login Required"),
            self.username_input,
            self.password_input,
            self.login_button,
            self.login_message,
            width=400,
            align='center'
        )

    def handle_login(self, event):
        """Handle login attempt"""
        username = self.username_input.value
        password = self.password_input.value

        if auth.authenticate(username, password):
            self.authenticated = True
            self.current_user = username
            self.login_message.object = f"✓ Login successful! Welcome, {username}"
            # Force update the main view
            self.main_view[0] = self.create_main_dashboard()
        else:
            self.login_message.object = "✗ Invalid username or password"
            self.password_input.value = ""

    def setup_dashboard(self):
        """Setup main dashboard"""
        self.view_selector = pn.widgets.RadioButtonGroup(
            name='View',
            options=['Consolidated', 'By Region', 'By Location'],
            value='Consolidated',
            button_type='primary'
        )

        self.region_selector = pn.widgets.Select(
            name='Region',
            options=['All'] + sorted(set(loc['region'] for loc in LOCATIONS.values())),
            value='All'
        )

        self.location_selector = pn.widgets.Select(
            name='Location',
            options=['All'] + sorted([(code, loc['name']) for code, loc in LOCATIONS.items()],
                                    key=lambda x: x[1]),
            value='All'
        )

        self.date_range = pn.widgets.DateRangeSlider(
            name='Date Range',
            start=datetime(2024, 1, 1),
            end=datetime.now(),
            value=(datetime(2024, 1, 1), datetime.now())
        )

        # Set up callbacks
        self.view_selector.param.watch(self.update_view, 'value')
        self.region_selector.param.watch(self.update_view, 'value')
        self.location_selector.param.watch(self.update_view, 'value')
        self.date_range.param.watch(self.update_view, 'value')

        # Main view (will be updated based on authentication)
        self.main_view = pn.Column()

    def create_main_dashboard(self):
        """Create the main dashboard view"""
        if not self.authenticated:
            return self.login_panel

        # Get data
        df = self.get_filtered_data()

        # Create visualizations
        summary_cards = self.create_summary_cards(df)
        charts = self.create_charts(df)
        data_table = self.create_data_table(df)

        # Sidebar
        sidebar = pn.Column(
            pn.pane.Markdown(f"### Welcome, {self.current_user}"),
            pn.pane.Markdown("---"),
            self.view_selector,
            self.region_selector if self.view_selector.value == 'By Region' else None,
            self.location_selector if self.view_selector.value == 'By Location' else None,
            self.date_range,
            pn.pane.Markdown("---"),
            pn.pane.Markdown("#### Quick Stats"),
            summary_cards,
            width=300,
        )

        # Main content
        main_content = pn.Column(
            pn.pane.Markdown(f"# {DASHBOARD_TITLE}"),
            pn.pane.Markdown(f"## {self.get_view_title()}"),
            charts,
            pn.pane.Markdown("### Detailed Data"),
            data_table,
        )

        return pn.Row(sidebar, main_content)

    def get_view_title(self):
        """Get title based on current view"""
        if self.view_selector.value == 'Consolidated':
            return "All Locations Consolidated"
        elif self.view_selector.value == 'By Region':
            region = self.region_selector.value
            return f"Region: {region}" if region != 'All' else "All Regions"
        else:  # By Location
            loc = self.location_selector.value
            if loc == 'All':
                return "All Locations"
            else:
                return f"Location: {LOCATIONS[loc]['name']}"

    def get_filtered_data(self):
        """Get data based on current filters"""
        if self.view_selector.value == 'Consolidated':
            df = db.get_consolidated_data()
        elif self.view_selector.value == 'By Region':
            region = self.region_selector.value
            if region == 'All':
                df = db.get_all_data()
            else:
                df = db.get_data_by_region(region)
        else:  # By Location
            loc = self.location_selector.value
            if loc == 'All':
                df = db.get_all_data()
            else:
                df = db.get_data_by_location(loc)

        # Filter by date range if data exists
        if not df.empty and 'period_date' in df.columns:
            start_date, end_date = self.date_range.value
            df = df[(df['period_date'] >= pd.Timestamp(start_date)) &
                   (df['period_date'] <= pd.Timestamp(end_date))]

        return df

    def create_summary_cards(self, df):
        """Create summary stat cards"""
        if df.empty:
            return pn.pane.Markdown("*No data available*")

        stats = []

        # Calculate key metrics
        if 'amount' in df.columns:
            latest_revenue = df[df['line_item'] == 'Total Revenue']['amount'].sum()
            latest_net_income = df[df['line_item'] == 'Net Income']['amount'].sum()

            stats.append(f"**Total Revenue:** ${latest_revenue:,.2f}")
            stats.append(f"**Net Income:** ${latest_net_income:,.2f}")

            if latest_revenue > 0:
                margin = (latest_net_income / latest_revenue) * 100
                stats.append(f"**Profit Margin:** {margin:.1f}%")

        if 'location_code' in df.columns:
            location_count = df['location_code'].nunique()
            stats.append(f"**Locations:** {location_count}")

        return pn.pane.Markdown('\n\n'.join(stats))

    def create_charts(self, df):
        """Create visualization charts"""
        if df.empty:
            return pn.pane.Markdown("*No data available for visualization*")

        charts = []

        try:
            # Revenue trend over time
            if 'period_date' in df.columns and 'amount' in df.columns:
                revenue_df = df[df['line_item'] == 'Total Revenue'].copy()
                if not revenue_df.empty:
                    revenue_df = revenue_df.sort_values('period_date')
                    chart = revenue_df.hvplot.line(
                        x='period_date',
                        y='amount',
                        title='Revenue Trend',
                        xlabel='Date',
                        ylabel='Revenue ($)',
                        height=300,
                        responsive=True
                    )
                    charts.append(chart)

            # P&L breakdown (latest period)
            if 'line_item' in df.columns and 'amount' in df.columns:
                pnl_df = df.groupby('line_item')['amount'].sum().reset_index()
                pnl_df = pnl_df[pnl_df['amount'] != 0]  # Remove zero values

                if not pnl_df.empty:
                    chart = pnl_df.hvplot.bar(
                        x='line_item',
                        y='amount',
                        title='P&L Breakdown',
                        xlabel='',
                        ylabel='Amount ($)',
                        height=300,
                        rot=45,
                        responsive=True
                    )
                    charts.append(chart)

        except Exception as e:
            return pn.pane.Markdown(f"*Error creating charts: {e}*")

        if charts:
            return pn.Column(*charts)
        else:
            return pn.pane.Markdown("*Insufficient data for visualization*")

    def create_data_table(self, df):
        """Create interactive data table"""
        if df.empty:
            return pn.pane.Markdown("*No data available*")

        # Format the dataframe for display
        display_df = df.copy()

        # Format amounts
        if 'amount' in display_df.columns:
            display_df['amount'] = display_df['amount'].apply(
                lambda x: f"${x:,.2f}" if pd.notna(x) else ""
            )

        # Format dates
        if 'period_date' in display_df.columns:
            display_df['period_date'] = pd.to_datetime(display_df['period_date']).dt.strftime('%Y-%m')

        return pn.widgets.Tabulator(
            display_df,
            pagination='remote',
            page_size=20,
            sizing_mode='stretch_width',
            height=400
        )

    def update_view(self, event):
        """Update dashboard when filters change"""
        if self.authenticated:
            self.main_view[0] = self.create_main_dashboard()

    def get_template(self):
        """Get the main template"""
        self.main_view.append(
            self.create_main_dashboard() if self.authenticated else self.login_panel
        )
        return self.main_view


# Create dashboard instance
dashboard = PLDashboard()

# Create servable app
app = pn.template.FastListTemplate(
    title=DASHBOARD_TITLE,
    sidebar=[],
    main=[dashboard.get_template()],
    header_background='#1f77b4',
)

app.servable()


# For running locally
if __name__ == "__main__":
    pn.serve(
        app,
        port=DASHBOARD_PORT,
        show=True,
        title=DASHBOARD_TITLE,
        websocket_origin="*"
    )
