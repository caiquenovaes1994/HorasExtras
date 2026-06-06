
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_e2969558c2468a8a86965fc6e47e7615 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_a589c450b210bf9a22819d2c545a4324 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.bulk_delete", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["backgroundColor"] : "#800000", ["color"] : "white", ["&:hover"] : ({ ["backgroundColor"] : "#A30000" }), ["marginBottom"] : "1em" }),onClick:on_click_a589c450b210bf9a22819d2c545a4324},children)
    )
});
