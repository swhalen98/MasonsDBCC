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

# Industry Benchmarks for Restaurant Business
BENCHMARKS = {
    'food_cost_pct': 28.0,  # Ideal: 25-30%
    'labor_cost_pct': 30.0,  # Ideal: 25-35%
    'prime_cost_pct': 60.0,  # Ideal: 55-65% (Food + Labor)
    'gross_margin_pct': 65.0,  # Ideal: 60-70%
    'net_margin_pct': 10.0,  # Ideal: 8-15%
    'ebitda_margin_pct': 15.0,  # Ideal: 12-18%
    'opex_ratio_pct': 25.0,  # Ideal: 20-30%
}

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
            pn.pane.Markdown("#### Filters"),
            self.view_selector,
            self.region_selector if self.view_selector.value == 'By Region' else None,
            self.location_selector if self.view_selector.value == 'By Location' else None,
            self.date_range,
            pn.pane.Markdown("---"),
            pn.pane.Markdown("#### Key Performance Indicators"),
            summary_cards,
            width=350,
            scroll=True,
            styles={'background': '#f8f9fa', 'padding': '15px', 'border-radius': '5px'}
        )

        # Main content
        main_content = pn.Column(
            pn.pane.Markdown(f"# {DASHBOARD_TITLE}"),
            pn.pane.Markdown(f"## {self.get_view_title()}"),
            pn.layout.Divider(),
            charts,
            pn.layout.Divider(),
            pn.pane.Markdown("### Detailed Financial Data"),
            data_table,
            sizing_mode='stretch_width'
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

    def calculate_kpis(self, df):
        """Calculate key performance indicators"""
        if df.empty or 'line_item' not in df.columns:
            return {}

        # Aggregate by line item
        totals = df.groupby('line_item')['amount'].sum()

        # Get key values
        revenue = totals.get('Total Revenue', 0)
        cogs = totals.get('Cost of Goods Sold', 0)
        gross_profit = totals.get('Gross Profit', 0)
        labor = totals.get('Labor', 0)
        total_opex = totals.get('Total Operating Expenses', 0)
        net_income = totals.get('Net Income', 0)
        ebitda = totals.get('EBITDA', 0)

        kpis = {}

        if revenue > 0:
            # Calculate all KPIs
            kpis['revenue'] = revenue
            kpis['gross_margin_pct'] = (gross_profit / revenue) * 100
            kpis['food_cost_pct'] = (cogs / revenue) * 100
            kpis['labor_cost_pct'] = (labor / revenue) * 100
            kpis['prime_cost_pct'] = ((cogs + labor) / revenue) * 100
            kpis['net_margin_pct'] = (net_income / revenue) * 100
            kpis['ebitda_margin_pct'] = (ebitda / revenue) * 100 if ebitda != 0 else 0
            kpis['opex_ratio_pct'] = (total_opex / revenue) * 100

            # Calculate location count if available
            if 'location_code' in df.columns:
                location_count = df['location_code'].nunique()
                kpis['revenue_per_location'] = revenue / location_count if location_count > 0 else 0
                kpis['location_count'] = location_count

        return kpis

    def create_kpi_card(self, title, value, benchmark=None, format_type='percent', status_color=None):
        """Create a styled KPI card with benchmark comparison"""
        if format_type == 'percent':
            value_str = f"{value:.1f}%"
        elif format_type == 'currency':
            value_str = f"${value:,.0f}"
        else:
            value_str = f"{value:.0f}"

        # Determine status color based on benchmark
        if status_color is None and benchmark is not None:
            if format_type == 'percent':
                # For cost metrics (lower is better)
                if 'cost' in title.lower() or 'opex' in title.lower():
                    diff = value - benchmark
                    if diff <= -2:
                        status_color = '#28a745'  # Green - significantly better
                    elif diff <= 2:
                        status_color = '#ffc107'  # Yellow - within range
                    else:
                        status_color = '#dc3545'  # Red - needs attention
                # For margin metrics (higher is better)
                else:
                    diff = value - benchmark
                    if diff >= 2:
                        status_color = '#28a745'  # Green
                    elif diff >= -2:
                        status_color = '#ffc107'  # Yellow
                    else:
                        status_color = '#dc3545'  # Red
            else:
                status_color = '#007bff'  # Blue for non-comparable metrics

        if status_color is None:
            status_color = '#007bff'

        benchmark_str = f"<br><small style='color: #666;'>Benchmark: {benchmark:.1f}%</small>" if benchmark else ""

        card_html = f"""
        <div style='
            background: linear-gradient(135deg, {status_color}15 0%, {status_color}05 100%);
            border-left: 4px solid {status_color};
            padding: 15px;
            margin: 8px 0;
            border-radius: 4px;
        '>
            <div style='font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.5px;'>{title}</div>
            <div style='font-size: 24px; font-weight: bold; color: {status_color}; margin: 5px 0;'>{value_str}</div>
            {benchmark_str}
        </div>
        """
        return pn.pane.HTML(card_html, sizing_mode='stretch_width')

    def create_summary_cards(self, df):
        """Create KPI cards with benchmarks"""
        if df.empty:
            return pn.pane.Markdown("*No data available*")

        kpis = self.calculate_kpis(df)

        if not kpis:
            return pn.pane.Markdown("*Insufficient data for KPIs*")

        cards = []

        # Revenue & Net Margin (most important)
        if 'revenue' in kpis:
            cards.append(self.create_kpi_card(
                "Total Revenue",
                kpis['revenue'],
                format_type='currency',
                status_color='#007bff'
            ))

        if 'net_margin_pct' in kpis:
            cards.append(self.create_kpi_card(
                "Net Profit Margin",
                kpis['net_margin_pct'],
                benchmark=BENCHMARKS['net_margin_pct'],
                format_type='percent'
            ))

        # Prime Cost (Food + Labor) - Critical Restaurant Metric
        if 'prime_cost_pct' in kpis:
            cards.append(self.create_kpi_card(
                "Prime Cost %",
                kpis['prime_cost_pct'],
                benchmark=BENCHMARKS['prime_cost_pct'],
                format_type='percent'
            ))

        # Food Cost %
        if 'food_cost_pct' in kpis:
            cards.append(self.create_kpi_card(
                "Food Cost %",
                kpis['food_cost_pct'],
                benchmark=BENCHMARKS['food_cost_pct'],
                format_type='percent'
            ))

        # Labor Cost %
        if 'labor_cost_pct' in kpis:
            cards.append(self.create_kpi_card(
                "Labor Cost %",
                kpis['labor_cost_pct'],
                benchmark=BENCHMARKS['labor_cost_pct'],
                format_type='percent'
            ))

        # Gross Margin
        if 'gross_margin_pct' in kpis:
            cards.append(self.create_kpi_card(
                "Gross Margin %",
                kpis['gross_margin_pct'],
                benchmark=BENCHMARKS['gross_margin_pct'],
                format_type='percent'
            ))

        # EBITDA Margin
        if 'ebitda_margin_pct' in kpis:
            cards.append(self.create_kpi_card(
                "EBITDA Margin %",
                kpis['ebitda_margin_pct'],
                benchmark=BENCHMARKS['ebitda_margin_pct'],
                format_type='percent'
            ))

        # Operating Expense Ratio
        if 'opex_ratio_pct' in kpis:
            cards.append(self.create_kpi_card(
                "OpEx Ratio %",
                kpis['opex_ratio_pct'],
                benchmark=BENCHMARKS['opex_ratio_pct'],
                format_type='percent'
            ))

        # Revenue per Location
        if 'revenue_per_location' in kpis:
            cards.append(self.create_kpi_card(
                f"Avg Revenue/Location ({int(kpis.get('location_count', 0))} locs)",
                kpis['revenue_per_location'],
                format_type='currency',
                status_color='#17a2b8'
            ))

        return pn.Column(*cards, sizing_mode='stretch_width')

    def create_charts(self, df):
        """Create visualization charts"""
        if df.empty:
            return pn.pane.Markdown("*No data available for visualization*")

        charts = []

        try:
            # Revenue over time - Enhanced
            if 'period_date' in df.columns and 'amount' in df.columns:
                revenue_df = df[df['line_item'] == 'Total Revenue'].copy()
                if not revenue_df.empty and len(revenue_df) > 1:
                    revenue_df = revenue_df.groupby('period_date')['amount'].sum().reset_index()
                    revenue_df = revenue_df.sort_values('period_date')

                    chart = revenue_df.hvplot.line(
                        x='period_date',
                        y='amount',
                        title='Revenue Over Time',
                        xlabel='Period',
                        ylabel='Revenue ($)',
                        height=350,
                        width=800,
                        color='#1f77b4',
                        line_width=3,
                        responsive=True,
                        grid=True
                    ).opts(
                        fontsize={'title': 14, 'labels': 11, 'xticks': 9, 'yticks': 10}
                    )
                    charts.append(pn.pane.HoloViews(chart, sizing_mode='stretch_width'))

            # Net Income over time - Enhanced
            if 'period_date' in df.columns and 'amount' in df.columns:
                ni_df = df[df['line_item'] == 'Net Income'].copy()
                if not ni_df.empty and len(ni_df) > 1:
                    ni_df = ni_df.groupby('period_date')['amount'].sum().reset_index()
                    ni_df = ni_df.sort_values('period_date')

                    # Color based on positive/negative
                    chart = ni_df.hvplot.line(
                        x='period_date',
                        y='amount',
                        title='Net Income Over Time',
                        xlabel='Period',
                        ylabel='Net Income ($)',
                        height=350,
                        width=800,
                        color='#28a745',
                        line_width=3,
                        responsive=True,
                        grid=True
                    ).opts(
                        fontsize={'title': 14, 'labels': 11, 'xticks': 9, 'yticks': 10}
                    )
                    charts.append(pn.pane.HoloViews(chart, sizing_mode='stretch_width'))

            # KPI Trends over time (if multiple periods)
            if 'period_date' in df.columns and 'year' in df.columns and 'month' in df.columns:
                # Group by period and calculate KPIs per period
                periods = df.groupby(['year', 'month', 'period_date'])

                kpi_trends = []
                for (year, month, period), period_df in periods:
                    kpis = self.calculate_kpis(period_df)
                    if kpis:
                        kpis['period_date'] = period
                        kpi_trends.append(kpis)

                if len(kpi_trends) > 1:
                    kpi_df = pd.DataFrame(kpi_trends)
                    kpi_df = kpi_df.sort_values('period_date')

                    # Plot key margin trends
                    if all(col in kpi_df.columns for col in ['net_margin_pct', 'gross_margin_pct', 'prime_cost_pct']):
                        margin_chart = kpi_df.hvplot.line(
                            x='period_date',
                            y=['net_margin_pct', 'gross_margin_pct', 'prime_cost_pct'],
                            title='Key Margin Trends',
                            xlabel='Period',
                            ylabel='Percentage (%)',
                            height=350,
                            width=800,
                            legend='top_right',
                            line_width=2,
                            responsive=True,
                            grid=True
                        ).opts(
                            fontsize={'title': 14, 'labels': 11, 'xticks': 9, 'yticks': 10}
                        )
                        charts.append(pn.pane.HoloViews(margin_chart, sizing_mode='stretch_width'))

            # P&L breakdown (all periods combined)
            if 'line_item' in df.columns and 'amount' in df.columns:
                pnl_df = df.groupby('line_item')['amount'].sum().reset_index()
                pnl_df = pnl_df[pnl_df['amount'] != 0]  # Remove zero values

                # Filter to key line items for cleaner visualization
                key_items = ['Total Revenue', 'Cost of Goods Sold', 'Gross Profit', 'Labor',
                            'Total Operating Expenses', 'EBITDA', 'Net Income']
                pnl_df = pnl_df[pnl_df['line_item'].isin(key_items)]

                if not pnl_df.empty:
                    chart = pnl_df.hvplot.bar(
                        x='line_item',
                        y='amount',
                        title='P&L Summary (Period Total)',
                        xlabel='',
                        ylabel='Amount ($)',
                        height=350,
                        width=800,
                        rot=45,
                        color='#ff7f0e',
                        responsive=True,
                        grid=True
                    ).opts(
                        fontsize={'title': 14, 'labels': 11, 'xticks': 9, 'yticks': 10}
                    )
                    charts.append(pn.pane.HoloViews(chart, sizing_mode='stretch_width'))

        except Exception as e:
            return pn.pane.Markdown(f"*Error creating charts: {e}*")

        if charts:
            return pn.Column(
                pn.pane.Markdown("## Performance Charts"),
                *charts,
                sizing_mode='stretch_width'
            )
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
